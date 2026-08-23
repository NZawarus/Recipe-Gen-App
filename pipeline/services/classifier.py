import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Improved classification prompt for segmented images
CLASSIFICATION_PROMPT = """
You are an expert food identifier. Analyze the images provided and identify the food items present.

Instructions:
1. For each image, identify the main food item in the center of the photo.
2. Return ONLY the name of the food item for each image (e.g., "tomato", "chicken", "rice").
3. Skip any image that doesn't contain a recognizable food item.
4. Use generic food names (e.g., "apple" not "Granny Smith Apple").
5. Avoid brand names unless it's a unique product with no generic equivalent.
6. Separate each identified item with a comma.
7. Do not include any explanations or descriptions - just the comma-separated list.

Example response: "tomato, chicken, rice, pasta, onion"
"""

# Prompt for whole image classification
WHOLE_IMAGE_PROMPT = """
You are an expert at identifying food ingredients in images. Look at this image of food items and list all the ingredients you can identify.

Instructions:
1. Identify ALL food ingredients visible in the image.
2. List each ingredient using its generic name (e.g., "tomato" not "Roma tomato").
3. Avoid brand names unless it's a unique product.
4. Separate each item with a comma.
5. List up to 30 ingredients maximum.
6. Focus on raw ingredients rather than prepared dishes when possible.
7. If something appears to be a prepared dish and you can't clearly identify individual ingredients, name the dish.
8. Be as specific as possible while remaining accurate.
9. Do not include any explanations, descriptions, or categories - just the comma-separated list.

Example good response: "tomato, chicken breast, rice, onion, bell pepper, garlic"
Example bad response: "I can see tomatoes, what looks like chicken, and some herbs..."

Your response:
"""

class Classifier:
    def __init__(self, model="gemini-2.0-flash"):
        """
        Initialize the classifier with the Gemini model.
        
        Args:
            model (str): The Gemini model to use
        """
        self.model_name = model
        self.classifications = []
        self.setup()
        
    def setup(self):
        """Set up the Gemini API with authentication"""
        try:
            # Load API key from environment
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')
            
            if not api_key:
                logger.error("No GOOGLE_API_KEY found in environment")
                raise ValueError("Missing GOOGLE_API_KEY environment variable")
                
            # Configure the Gemini API
            genai.configure(api_key=api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized Gemini model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error setting up Gemini API: {str(e)}")
            raise

    def classify_whole_image(self, image):
        """
        Classify all food items in a single image.
        
        Args:
            image: PIL Image object of the whole image
            
        Returns:
            list: List of detected ingredient names
        """
        try:
            # Create content with the prompt and image
            prompt = [WHOLE_IMAGE_PROMPT, image]
            
            # Generate classifications using Gemini
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.warning("Empty response from Gemini")
                return []
                
            # Parse the classification results
            text_result = response.text.strip()
            
            # Split by comma and clean up
            ingredients = [item.strip() for item in text_result.split(',')]
            
            # Filter out empty strings
            ingredients = [item for item in ingredients if item]
            
            return ingredients
            
        except Exception as e:
            logger.error(f"Error classifying whole image: {str(e)}")
            return []

    def classify_imgs(self, masks):
        """
        Classify food items in the provided image masks.
        
        Args:
            masks (list): List of PIL Image objects
        
        Returns:
            list: List of classified food items
        """
        try:
            if not masks:
                logger.warning("No masks provided for classification")
                return self.classifications
                
            # Create content parts with the prompt and images
            prompt = [CLASSIFICATION_PROMPT]
            for img in masks:
                prompt.append(img)
                
            logger.info(f"Classifying {len(masks)} mask images")
            
            # Generate classifications using Gemini
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.warning("Empty response from Gemini")
                return self.classifications
                
            # Parse the classification results
            text_result = response.text.strip()
            logger.info(f"Raw classification result: {text_result}")
            
            # Split by comma and clean up
            ingredients = [item.strip() for item in text_result.split(',')]
            
            # Filter out empty strings
            ingredients = [item for item in ingredients if item]
            
            self.classifications = ingredients
            logger.info(f"Classified {len(ingredients)} ingredients: {ingredients}")
            
            return self.classifications
            
        except Exception as e:
            logger.error(f"Error classifying images: {str(e)}")
            return self.classifications

    def clear_output(self):
        """Clear the stored classifications"""
        self.classifications = []

    def get_classifications(self):
        """Return the current list of classifications"""
        return self.classifications


