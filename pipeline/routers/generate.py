from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Dict, Any
import base64
import os
import logging
import json
import traceback
import uuid
from services.pipeline_service import FridgeToRecipe

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize the FridgeToRecipe pipeline
gemini_model = "gemini-2.0-flash"
fridge_to_recipe = FridgeToRecipe(
    gemini_model, 
    max_image_dimension=1000,
    use_gemini_for_recipes=True  # Use Gemini for recipe generation by default
)

class ImageInfo(BaseModel):
    filename: str
    image_data: str

class RecipeRequest(BaseModel):
    images: List[ImageInfo]
    servings: int = 2

@router.post("/generate_recipe")
async def generate_recipe(
    request: RecipeRequest = Body(...),
    use_llama: bool = Query(False, description="Set to true to use Llama instead of Gemini for recipe generation"),
    skip_segmentation: bool = Query(False, description="Set to true to skip segmentation and use whole image classification only")
) -> dict:
    """
    Generate a recipe from multiple uploaded images.
    
    Args:
        request: Contains list of base64 encoded images and servings parameter
        use_llama: If true, use Llama instead of Gemini for recipe generation
        skip_segmentation: If true, skip segmentation and use whole image classification only
        
    Returns:
        dict: The generated recipe and detected ingredients
    """
    try:
        logger.info(f"Received image upload request with {len(request.images)} images")
        logger.info(f"Using {'Llama' if use_llama else 'Gemini'} for recipe generation")
        logger.info(f"Segmentation is {'disabled' if skip_segmentation else 'enabled'}")
        
        # Create a new FridgeToRecipe instance with the specified recipe generator
        if use_llama:
            pipeline = FridgeToRecipe(
                gemini_model, 
                max_image_dimension=1000,
                use_gemini_for_recipes=False  # Use Llama
            )
        else:
            pipeline = fridge_to_recipe  # Use the default (Gemini)
        
        # Ensure SavedImages directory exists
        os.makedirs("SavedImages", exist_ok=True)
        
        # Get parameters from request
        images = request.images
        servings = request.servings
        
        # Process each image and collect all ingredients
        all_ingredients = []
        image_paths = []
        
        # Save and process each image
        for image_info in images:
            try:
                # Generate a unique ID for this image if filename is duplicated
                unique_id = str(uuid.uuid4())[:8]
                filename = f"{unique_id}_{image_info.filename}"
                
                # Decode the base64 image
                img_bytes = base64.b64decode(image_info.image_data)
                
                # Save the image
                image_path = f"SavedImages/{filename}"
                with open(image_path, "wb") as f:
                    f.write(img_bytes)
                logger.info(f"Image saved successfully to {image_path}")
                
                # Scale the image
                pipeline.scale_image(image_path)
                
                # Process the image - either with segmentation or whole image
                if skip_segmentation:
                    ingredients = pipeline.classify_whole_image(image_path)
                else:
                    ingredients = pipeline.segment_and_classify(image_path)
                
                if ingredients:
                    all_ingredients.extend(ingredients)
                    
                # Add to image paths list
                image_paths.append(image_path)
                
            except Exception as e:
                logger.error(f"Error processing image {image_info.filename}: {str(e)}")
                # Continue with other images even if one fails
        
        # Remove duplicates from ingredients list
        all_ingredients = list(set(all_ingredients))
        
        logger.info(f"All ingredients detected: {all_ingredients}")
        
        # If no ingredients were detected in any image
        if not all_ingredients:
            return {
                "ingredients": [],
                "recipe": {
                    "title": "No Ingredients Detected",
                    "servings": servings,
                    "recipe_ingredients": [],
                    "calories": 0,
                    "instructions": [
                        "No ingredients were detected in any of the uploaded images.",
                        "Please try again with clearer images of food items."
                    ]
                },
                "generator_used": "llama" if use_llama else "gemini",
                "segmentation_used": not skip_segmentation
            }
        
        # Generate recipe from all detected ingredients
        try:
            recipe = pipeline.generate_recipe(all_ingredients, servings)
            
            # Parse the recipe string as JSON if it's a string
            if isinstance(recipe, str):
                try:
                    recipe_json = json.loads(recipe)
                except json.JSONDecodeError:
                    recipe_json = recipe
            else:
                recipe_json = recipe
            
            logger.info("Recipe generated successfully")
            return {
                "ingredients": all_ingredients,
                "recipe": recipe_json,
                "generator_used": "llama" if use_llama else "gemini",
                "segmentation_used": not skip_segmentation
            }
            
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Return an error instead of a default recipe
            raise HTTPException(
                status_code=500, 
                detail=f"Recipe generation failed: {str(e)}"
            )
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
