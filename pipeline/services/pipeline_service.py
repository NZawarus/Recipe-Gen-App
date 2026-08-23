from .segmenter import SegmenterModel
from .classifier import Classifier
from PIL import Image
from services.llama_recipe_generator import LlamaRecipeGenerator
from services.gemini_recipe_generator import GeminiRecipeGenerator
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Configuration constants
CROPPED_IMAGES_DIR = "crops/"
MINIMUM_MASK_AREA = 200
SAVE_CROPS = True

class FridgeToRecipe:
    """
    Main pipeline class that handles the entire process from image to recipe:
    1. Image input
    2. FastSAM segmentation
    3. Gemini classification of segmented regions
    4. Gemini/Llama recipe generation
    """
    def __init__(self, gemini_model, max_image_dimension=1000, use_gemini_for_recipes=True):
        # Ensure crops directory exists
        os.makedirs(CROPPED_IMAGES_DIR, exist_ok=True)
        
        # Initialize components
        self.segmenter = SegmenterModel(
            cropped_images_dir=CROPPED_IMAGES_DIR,
            save_crops=SAVE_CROPS,
            minimum_mask_area=MINIMUM_MASK_AREA
        )
        self.classifier = Classifier(gemini_model)
        
        # Choose recipe generator based on parameter
        self.use_gemini_for_recipes = use_gemini_for_recipes
        if use_gemini_for_recipes:
            logger.info("Using Gemini for recipe generation")
            self.recipe_generator = GeminiRecipeGenerator()
        else:
            logger.info("Using Llama for recipe generation")
            self.recipe_generator = LlamaRecipeGenerator()
            
        self.max_image_dimension = max_image_dimension

    def scale_image(self, img_path):
        """Scale the input image to fit within max dimensions"""
        with Image.open(img_path) as image:
            width, height = image.size

            # Scale down if needed
            if width >= height and width > self.max_image_dimension:
                new_width = self.max_image_dimension
                new_height = height * (new_width / width)
                resized_image = image.resize((int(new_width), int(new_height)))
                resized_image.save(img_path)
            elif height > width and height > self.max_image_dimension:
                new_height = self.max_image_dimension
                new_width = width * (new_height / height)
                resized_image = image.resize((int(new_width), int(new_height)))
                resized_image.save(img_path)
    
    def classify_whole_image(self, img_path):
        """Classify food items in the entire image using Gemini"""
        try:
            # Open the image
            image = Image.open(img_path)
            
            # Classify the image directly with Gemini
            classifications = self.classifier.classify_whole_image(image)
            return classifications
        except Exception as e:
            logger.error(f"Error classifying whole image: {str(e)}")
            return []

    def segment_and_classify(self, img_path):
        """Segment the image and classify each segment"""
        try:
            logger.info(f"Starting segmentation and classification for {img_path}")
            
            # First, segment the image using FastSAM
            crops = self.segmenter.segment_sample(img_path)
            
            if not crops:
                logger.warning(f"No segments found in {img_path}, falling back to whole image classification")
                return self.classify_whole_image(img_path)
            
            logger.info(f"Found {len(crops)} segments to classify")
            
            # Classify the crops using Gemini
            self.classifier.classify_imgs(crops)
            classifications = self.classifier.get_classifications()
            
            # Clean up after classification
            self.classifier.clear_output()
            self.segmenter.clear_crops()
            
            # Remove duplicates
            unique_classifications = list(set(classifications))
            logger.info(f"Identified ingredients: {unique_classifications}")
            
            return unique_classifications
        except Exception as e:
            logger.error(f"Error in segment_and_classify: {str(e)}")
            # Fallback to whole image classification
            logger.info("Falling back to whole image classification")
            return self.classify_whole_image(img_path)
        
    def generate_recipe(self, classifications, servings=2, cuisine="any"):
        """Generate a recipe based on the classified ingredients"""
        if self.use_gemini_for_recipes:
            # Use Gemini recipe generator
            return self.recipe_generator.generate_recipe(
                ingredients=classifications,
                servings=servings
            )
        else:
            # Use Llama recipe generator
            return self.recipe_generator.generate_recipe_simple(
                ingredients=classifications,
                servings=servings
            )
        
    def process_image_to_recipe(self, img_path, servings=2, cuisine="any"):
        """
        End-to-end pipeline to process an image and return a recipe
        """
        # Step 1: Scale the image if needed
        self.scale_image(img_path)
        
        # Step 2: Segment and classify the image
        classifications = self.segment_and_classify(img_path)
        
        # If no ingredients detected, return an error message
        if not classifications:
            return {
                "ingredients_detected": [],
                "recipe": {
                    "title": "No Ingredients Detected",
                    "servings": servings,
                    "recipe_ingredients": [],
                    "calories": 0,
                    "instructions": [
                        "No ingredients were detected in the image.",
                        "Please try again with a clearer image of food items."
                    ]
                }
            }
        
        # Step 3: Generate a recipe
        recipe = self.generate_recipe(classifications, servings, cuisine)
        return {
            "ingredients_detected": classifications,
            "recipe": recipe
        }

    def segment_image(self, img_path, img_num=1):
        """Segment the image using SAM2 and return the crops (kept for backward compatibility)"""
        self.segmenter.segment_sample(img_path, img_num)
        crops = self.segmenter.get_crops()
        return crops

    def process_images(self, crops):
        """Process the segmented images to extract ingredient classifications (kept for backward compatibility)"""
        self.classifier.classify_imgs(crops)
        classifications = self.classifier.get_classifications()
        self.classifier.clear_output()
        return classifications