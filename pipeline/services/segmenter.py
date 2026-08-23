import time
import os
import cv2
import numpy as np
import torch
from PIL import Image
import supervision as sv
import requests
import logging
from ultralytics import YOLO
import hashlib
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crop is extended in each direction by x pixels
CROP_EXTENSION = 50
FASTSAM_MODEL_URL = "https://github.com/CASIA-IVA-Lab/FastSAM/releases/download/FastSAM-s/FastSAM-s.pt"
FASTSAM_MODEL_PATH = "FastSAM-s.pt"
# Fallback to YOLO if FastSAM fails
YOLO_MODEL_PATH = "yolov8n-seg.pt"

class SegmenterModel:
    def __init__(self, model_path=None, cropped_images_dir="crops/", save_crops=True, minimum_mask_area=200):
        self.crops = []
        self.cropped_images_dir = cropped_images_dir
        self.save_crops = save_crops
        self.minimum_mask_area = minimum_mask_area
        self.setup_gpu()
        
        # Try to use FastSAM first, fallback to YOLO if it fails
        try:
            self.use_fastsam = True
            self.setup_fastsam()
        except Exception as e:
            logger.error(f"FastSAM initialization failed: {str(e)}")
            logger.info("Falling back to YOLOv8 for segmentation")
            self.use_fastsam = False
            self.setup_yolo()
        
    def setup_gpu(self):
        # select the device for computation
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        logger.info(f"Using device: {self.device}")

    def verify_file(self, file_path, expected_size_mb=None):
        """Verify if a file exists and has a reasonable size"""
        if not os.path.exists(file_path):
            return False
            
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        if expected_size_mb and file_size < expected_size_mb * 0.9:  # Allow for some margin
            logger.warning(f"File {file_path} is too small: {file_size:.2f}MB < {expected_size_mb}MB")
            return False
            
        return True

    def download_model(self, url, dest_path, expected_size_mb=None):
        """Download a model with progress tracking and verification"""
        try:
            # Remove file if it exists but is too small
            if os.path.exists(dest_path):
                if not self.verify_file(dest_path, expected_size_mb):
                    logger.warning(f"Removing potentially corrupt file: {dest_path}")
                    os.remove(dest_path)
                else:
                    logger.info(f"Using existing model file: {dest_path}")
                    return True
            
            # Download the file
            logger.info(f"Downloading model from {url} to {dest_path}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            total_size = int(response.headers.get('content-length', 0))
            total_size_mb = total_size / (1024 * 1024)
            
            # Check size before downloading
            if expected_size_mb and total_size_mb < expected_size_mb * 0.9:
                logger.warning(f"Remote file size ({total_size_mb:.2f}MB) is less than expected ({expected_size_mb}MB)")
            
            # Download with progress reporting
            downloaded_size = 0
            last_log_time = 0
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progress every 5 seconds
                        current_time = time.time()
                        if current_time - last_log_time > 5:
                            downloaded_mb = downloaded_size / (1024 * 1024)
                            logger.info(f"Downloaded {downloaded_mb:.2f}MB / {total_size_mb:.2f}MB ({100 * downloaded_size / total_size:.1f}%)")
                            last_log_time = current_time
            
            # Verify the download
            if not self.verify_file(dest_path, expected_size_mb):
                logger.error(f"Downloaded file {dest_path} failed verification")
                return False
                
            logger.info(f"Model downloaded successfully to {dest_path}")
            return True
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            return False

    def setup_fastsam(self):
        """Initialize the FastSAM model"""
        try:
            # Download or verify the model (FastSAM is ~100 MB)
            if not self.download_model(FASTSAM_MODEL_URL, FASTSAM_MODEL_PATH, expected_size_mb=90):
                raise ValueError("Failed to download or verify FastSAM model")
            
            # Attempt to import FastSAM class
            try:
                from ultralytics import FastSAM
                # Load the Fast SAM model
                self.model = FastSAM(FASTSAM_MODEL_PATH)
                logger.info("FastSAM model loaded successfully")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to import FastSAM: {str(e)}")
                raise ValueError(f"FastSAM not available in your ultralytics version: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error setting up FastSAM: {str(e)}")
            raise

    def setup_yolo(self):
        """Initialize YOLOv8 as a fallback for segmentation"""
        try:
            # Check if YOLO model exists or download it
            if not os.path.exists(YOLO_MODEL_PATH):
                self.model = YOLO("yolov8n-seg.pt")  # This will download automatically
            else:
                self.model = YOLO(YOLO_MODEL_PATH)
                
            logger.info("YOLOv8 model loaded successfully as fallback")
        except Exception as e:
            logger.error(f"Error setting up YOLOv8: {str(e)}")
            raise

    def generate_masks(self, image_path):
        """Generate masks using either FastSAM or YOLOv8"""
        try:
            # Read the original image first
            orig_img = cv2.imread(image_path)
            if orig_img is None:
                raise ValueError(f"Failed to read image: {image_path}")
                
            # Run the appropriate model
            logger.info(f"Generating masks for image: {image_path} using {'FastSAM' if self.use_fastsam else 'YOLOv8'}")
            results = self.model(image_path, device=self.device.type)
            
            # Process the masks from the results
            filtered_masks = []
            
            # Extract masks from the results - handle both model types
            if hasattr(results[0], 'masks') and results[0].masks is not None:
                # Both FastSAM and YOLOv8 have this structure
                masks_data = results[0].masks.data
                if hasattr(masks_data, 'cpu'):
                    masks_data = masks_data.cpu().numpy()
                else:
                    masks_data = np.array(masks_data)
                    
                # Process each mask
                for i in range(len(masks_data)):
                    mask = masks_data[i]
                    # Calculate mask area (count of True pixels)
                    area = np.count_nonzero(mask)
                    if area > self.minimum_mask_area:
                        filtered_masks.append(mask)
            else:
                # Alternative approach using bounding boxes
                logger.warning("No masks found in results, using bounding boxes instead")
                if hasattr(results[0], 'boxes') and results[0].boxes is not None:
                    # Create masks from bounding boxes
                    boxes = results[0].boxes.xyxy  # Using xyxy format
                    if hasattr(boxes, 'cpu'):
                        boxes = boxes.cpu().numpy()
                    else:
                        boxes = np.array(boxes)
                        
                    for box in boxes:
                        # Create a mask from the bounding box
                        height, width = orig_img.shape[:2]
                        mask = np.zeros((height, width), dtype=np.uint8)
                        x1, y1, x2, y2 = map(int, box[:4])
                        mask[y1:y2, x1:x2] = 1
                        
                        # Calculate area
                        area = (x2 - x1) * (y2 - y1)
                        if area > self.minimum_mask_area:
                            filtered_masks.append(mask)
            
            # If no masks found, create one mask for the whole image
            if not filtered_masks:
                logger.warning("No masks found, creating a mask for the whole image")
                height, width = orig_img.shape[:2]
                whole_mask = np.ones((height, width), dtype=np.uint8)
                filtered_masks.append(whole_mask)
            
            logger.info(f"Generated {len(filtered_masks)} masks after filtering")
            return filtered_masks, orig_img
        except Exception as e:
            logger.error(f"Error generating masks: {str(e)}")
            # Create a fallback mask for the whole image
            height, width = orig_img.shape[:2]
            whole_mask = np.ones((height, width), dtype=np.uint8)
            return [whole_mask], orig_img

    def crop_masks(self, masks, orig_img):
        """Extract crops from the original image based on mask bounding boxes"""
        img_height, img_width = orig_img.shape[:2]
        self.crops = []
        
        for i, mask in enumerate(masks):
            try:
                # Ensure mask is binary and has the right shape
                if mask.shape[:2] != (img_height, img_width):
                    logger.warning(f"Mask shape {mask.shape} does not match image shape {(img_height, img_width)}")
                    continue
                    
                # Ensure mask is binary
                if not mask.dtype == np.bool_:
                    mask = mask > 0
                    
                # Get bounding box from mask
                # Find rows and columns where mask is True
                y_indices, x_indices = np.where(mask)
                
                if len(y_indices) == 0 or len(x_indices) == 0:
                    logger.warning(f"Empty mask for crop {i}, skipping")
                    continue  # Skip empty masks
                    
                # Get the bounding box coordinates
                y_min, y_max = np.min(y_indices), np.max(y_indices)
                x_min, x_max = np.min(x_indices), np.max(x_indices)
                
                # Extend crop to capture surrounding area
                x_min = max(0, x_min - CROP_EXTENSION)
                y_min = max(0, y_min - CROP_EXTENSION)
                x_max = min(img_width, x_max + CROP_EXTENSION)
                y_max = min(img_height, y_max + CROP_EXTENSION)
                
                # Ensure valid coordinates
                if x_min >= x_max or y_min >= y_max:
                    logger.warning(f"Invalid crop coordinates: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")
                    continue
                    
                # Crop the image
                crop = orig_img[y_min:y_max, x_min:x_max]
                
                # Convert to RGB for PIL
                crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image for compatibility with the existing pipeline
                crop_pil = Image.fromarray(crop_rgb)
                self.crops.append(crop_pil)
                
                # Save the crop if needed
                if self.save_crops:
                    crop_filename = f"mask{i+1}.png"
                    crop_path = os.path.join(self.cropped_images_dir, crop_filename)
                    cv2.imwrite(crop_path, crop)
                    logger.info(f"Saved crop to {crop_path}")
            except Exception as e:
                logger.error(f"Error processing crop {i}: {str(e)}")
                continue
                
        return self.crops

    def segment_sample(self, img_path, img_num=1):
        """Segment an image using FastSAM or YOLOv8"""
        try:
            # Ensure crops directory exists
            os.makedirs(self.cropped_images_dir, exist_ok=True)
            
            # Generate masks
            segment_start = time.time()
            masks, orig_img = self.generate_masks(img_path)
            segment_end = time.time()
            logger.info(f"Segmentation time: {segment_end - segment_start:.2f} seconds")
            
            # Create crops based on masks
            crop_start = time.time()
            self.crop_masks(masks, orig_img)
            crop_end = time.time()
            logger.info(f"Cropping time: {crop_end - crop_start:.2f} seconds")
            
            # If no crops were generated, use the whole image
            if not self.crops:
                logger.info("No valid crops found, using whole image")
                img = Image.open(img_path)
                self.crops = [img]
            
            return self.crops
        except Exception as e:
            logger.error(f"Error in segmentation: {str(e)}")
            # Return the whole image as a fallback
            try:
                img = Image.open(img_path)
                self.crops = [img]
                return self.crops
            except Exception as e2:
                logger.error(f"Could not open image as fallback: {str(e2)}")
                return []

    def segment_samples(self, img_paths):
        """Segment multiple images"""
        all_crops = []
        for i, img_path in enumerate(img_paths):
            crops = self.segment_sample(img_path, i+1)
            all_crops.extend(crops)
        return all_crops

    def clear_output(self):
        """Clear all saved crops"""
        for filename in os.listdir(self.cropped_images_dir):
            file_path = os.path.join(self.cropped_images_dir, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {str(e)}")

    def get_crops(self):
        """Get the generated crops"""
        return self.crops
    
    def clear_crops(self):
        """Clear the current crops list"""
        self.crops = []
        