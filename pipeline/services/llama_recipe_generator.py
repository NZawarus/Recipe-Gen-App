import transformers
import torch
import json
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple recipe prompt
RECIPE_PROMPT = """Generate a recipe using the following ingredients: {ingredients}.
You can use additional common ingredients like salt, pepper, or spices as needed.
Please include:
1. Recipe title
2. Servings: {servings}
3. Ingredients with quantities
4. Cooking instructions
5. Estimated calories per serving

IMPORTANT: Your response MUST be VALID JSON. Do not include markdown or code block formatting.
Format your response as a SINGLE valid JSON object EXACTLY like this:
{{
  "title": "Recipe Title",
  "servings": {servings},
  "recipe_ingredients": [
    {{"ingredient": "First Ingredient", "quantity": "amount"}},
    {{"ingredient": "Second Ingredient", "quantity": "amount"}}
  ],
  "calories": 123,
  "instructions": [
    "First instruction step",
    "Second instruction step"
  ]
}}
"""

class LlamaRecipeGenerator:
    def __init__(self):
        self.setup_llama()

    def setup_llama(self):
        # Set up device (CUDA, MPS, or CPU)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        logger.info(f"Using device: {self.device}")

        # Using a smaller Llama model for better performance
        self.model_id = "meta-llama/Llama-3.2-3B-Instruct"
        
        # Set up the text generation pipeline
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
        )

    def generate_recipe_simple(self, ingredients, servings=2, cuisine="any"):
        """
        Generate a recipe based on the given ingredients using a simple prompt approach
        without RAG or embeddings.
        
        Args:
            ingredients (list): List of ingredient names
            servings (int): Number of servings
            cuisine (str): Desired cuisine type (ignored in this version)
            
        Returns:
            str: Generated recipe in JSON format
        """
        # Remove duplicates and join ingredients
        ingredients = list(set(ingredients))
        ingredients_str = ", ".join(ingredients)
        
        logger.info(f"Generating recipe for ingredients: {ingredients_str}")
        
        # Format the prompt (ignoring cuisine parameter)
        prompt = RECIPE_PROMPT.format(
            ingredients=ingredients_str,
            servings=servings
        )
        
        # Generate the recipe using the Llama model
        messages = [{"role": "user", "content": prompt}]
        
        try:
            outputs = self.pipeline(
                messages, 
                max_new_tokens=2048,
                temperature=0.7,  # Add some creativity
                top_p=0.9,        # Use nucleus sampling
            )
            
            # Extract the generated text
            result = outputs[0]["generated_text"][-1]["content"].strip()
            logger.info("Successfully generated recipe text")
            logger.debug(f"Raw model output: {result}")
            
            # Try to extract valid JSON
            try:
                # Try direct loading first (best case scenario)
                try:
                    recipe_json = json.loads(result)
                    return json.dumps(recipe_json, indent=2)
                except json.JSONDecodeError:
                    pass
                
                # Find JSON-like structure - look for opening and closing braces
                json_pattern = re.search(r'(\{.*\})', result, re.DOTALL)
                if json_pattern:
                    potential_json = json_pattern.group(1)
                    try:
                        # Clean up potential JSON
                        cleaned_json = self._clean_json_string(potential_json)
                        recipe_json = json.loads(cleaned_json)
                        return json.dumps(recipe_json, indent=2)
                    except json.JSONDecodeError:
                        logger.warning("JSON structure found but parsing failed")
                        # Continue to fallback
                
                # Try to extract by finding keys if we can't parse properly
                if '"title"' in result or "'title'" in result:
                    logger.warning("Using manual JSON construction from extracted values")
                    title_match = re.search(r'"title"\s*:\s*"([^"]+)"', result)
                    title = title_match.group(1) if title_match else f"Recipe with {ingredients_str.split(',')[0]}"
                    
                    # Create manual recipe
                    manual_recipe = {
                        "title": title,
                        "servings": servings,
                        "recipe_ingredients": [
                            {"ingredient": ingredient.strip(), "quantity": "as needed"} 
                            for ingredient in ingredients_str.split(',')
                        ],
                        "calories": 0,
                        "instructions": [
                            "Combine ingredients and prepare as desired"
                        ]
                    }
                    return json.dumps(manual_recipe, indent=2)
                
                # If we can't find any valid JSON structure, use fallback
                logger.error("No JSON structure found in model output")
                return self._create_fallback_recipe(ingredients_str, servings)
                
            except Exception as e:
                logger.error(f"Error parsing JSON from model output: {str(e)}")
                # In case of JSON parsing error, return a fallback recipe
                return self._create_fallback_recipe(ingredients_str, servings)
                
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            return self._create_fallback_recipe(ingredients_str, servings)
    
    def _clean_json_string(self, json_str):
        """Clean up a JSON string to improve parsing chances"""
        # Remove markdown code block indicators if present
        json_str = re.sub(r'```json|```', '', json_str)
        
        # Normalize quotes (replace curly quotes with straight quotes)
        json_str = json_str.replace('"', '"').replace('"', '"')
        json_str = json_str.replace("'", "'").replace("'", "'")
        
        # Remove any leading/trailing whitespace or newlines
        json_str = json_str.strip()
        
        # Replace any escaped newlines
        json_str = json_str.replace('\\n', ' ')
        
        return json_str
    
    def _create_fallback_recipe(self, ingredients_str, servings):
        """Create a fallback recipe when model output can't be parsed"""
        fallback_recipe = {
            "title": f"Fruit Salad with {ingredients_str.split(',')[0]}",
            "servings": servings,
            "recipe_ingredients": [
                {"ingredient": ingredient.strip(), "quantity": "as needed"} 
                for ingredient in ingredients_str.split(',')
            ],
            "calories": 0,
            "instructions": [
                f"Combine all fruit: {ingredients_str}",
                "Mix well in a large bowl",
                "Add honey or sugar to taste if desired",
                "Refrigerate for 30 minutes before serving",
                "Enjoy your fruit salad!"
            ]
        }
        return json.dumps(fallback_recipe, indent=2)
            
    # Keep the old method for backward compatibility but just call the new one
    def generate_recipe(self, num_recipe, ingredients, ingredients_used, new_ingredients, servings, cuisine, ingredient_blacklist):
        """Legacy method maintained for backward compatibility"""
        return self.generate_recipe_simple(ingredients, servings)

