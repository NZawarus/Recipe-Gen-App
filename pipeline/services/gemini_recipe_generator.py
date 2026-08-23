import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import json
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Recipe generation prompt
RECIPE_PROMPT = """
Create a complete recipe using some of these ingredients: {ingredients}.
Only use ingredients that make sense in a recipe together.
You may add other ingredients as needed, but only if they make sense in the context of the recipe.
Assume basic ingredients like salt, pepper, and spices are available.

For the recipe, include:
1. A title
2. Number of servings: {servings}
3. List of all ingredients with quantities
4. Step-by-step cooking instructions
5. Estimated calories per serving

IMPORTANT: Your response MUST be a WELL-FORMED JSON object with NO leading/trailing characters or newlines.
Format in EXACTLY this structure:
{{
  "title": "The recipe title",
  "servings": {servings},
  "recipe_ingredients": [
    {{"ingredient": "name of ingredient", "quantity": "amount"}},
    {{"ingredient": "name of ingredient", "quantity": "amount"}}
  ],
  "calories": 123,
  "instructions": [
    "First instruction step",
    "Second instruction step",
    "Third instruction step"
  ]
}}

Do not include any explanations, markdown formatting, or text before or after the JSON.
"""

class GeminiRecipeGenerator:
    def __init__(self, model_name="gemini-1.5-flash"):
        """
        Initialize the recipe generator with the Gemini model.
        
        Args:
            model_name (str): The Gemini model to use
        """
        self.model_name = model_name
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
            
            # Initialize the model - using Pro for better reasoning
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized Gemini model for recipe generation: {self.model_name}")
        except Exception as e:
            logger.error(f"Error setting up Gemini API: {str(e)}")
            raise

    def generate_recipe(self, ingredients, servings=2):
        """
        Generate a recipe based on the given ingredients.
        
        Args:
            ingredients (list): List of ingredient names
            servings (int): Number of servings
            
        Returns:
            str: Generated recipe in JSON format
        """
        try:
            # Remove duplicates and join ingredients
            ingredients = list(set(ingredients))
            ingredients_str = ", ".join(ingredients)
            
            # Format the prompt
            prompt = RECIPE_PROMPT.format(
                ingredients=ingredients_str,
                servings=servings
            )
            
            # Generate recipe using Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    response_mime_type="application/json"
                )
            )
            
            if not response or not response.text:
                logger.warning("Empty response from Gemini")
                raise ValueError("Empty response from Gemini model")
            
            result = response.text.strip()
            
            # Try to parse as JSON
            json_text = self._clean_json_string(result)
            
            # Try different JSON extraction methods
            try:
                # Method 1: Direct parsing
                recipe_json = json.loads(json_text)
                return json.dumps(recipe_json, indent=2)
            except json.JSONDecodeError:
                # Method 2: Find JSON pattern
                json_pattern = re.search(r'(\{.*\})', json_text, re.DOTALL)
                if json_pattern:
                    try:
                        json_extract = json_pattern.group(1)
                        recipe_json = json.loads(json_extract)
                        return json.dumps(recipe_json, indent=2)
                    except json.JSONDecodeError:
                        pass
                
                # If we get here, we couldn't parse the JSON
                logger.error(f"Failed to parse recipe JSON: {json_text}")
                raise ValueError("Invalid JSON format in recipe generation response")
                
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            raise ValueError(f"Recipe generation failed: {str(e)}")
    
    def _clean_json_string(self, json_str):
        """Clean up a JSON string to improve parsing chances"""
        # Remove markdown code block indicators if present
        json_str = re.sub(r'```json|```', '', json_str)
        
        # Remove any leading/trailing whitespace or newlines
        json_str = json_str.strip()
        
        # Replace escaped newlines
        json_str = json_str.replace('\\n', ' ')
        
        # Remove extra quotes or other problematic characters
        json_str = json_str.replace('"{', '{').replace('}"', '}')
        
        return json_str 