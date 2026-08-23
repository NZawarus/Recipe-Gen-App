from segmenter import SegmenterModel
from classifier import Classifier
from PIL import Image
from llama_recipe_generator import LlamaRecipeGenerator
import os

# Replace These with final directory locations
SOURCE_IMAGES_DIR = "Images/Demo/"
SAM_MODEL_DIR = "SAM/sam2.1_hiera_large.pt"

# Sets whether cropped images should be saved
SAVE_CROPS = True
CROPPED_IMAGES_DIR = "Images/Crops/"

# Sets the minimum area a mask must take up to be used in classification
MINIMUM_MASK_AREA = 200

class FridgeToRecipe:

    def __init__(self, gemini_model, max_image_dimension):
        self.segmenter = SegmenterModel(SAM_MODEL_DIR, CROPPED_IMAGES_DIR, SAVE_CROPS, MINIMUM_MASK_AREA)
        self.classifier = Classifier(gemini_model)
        # self.recipe_generator = RecipeGenerator()
        self.recipe_generator = LlamaRecipeGenerator()
        self.max_image_dimension = max_image_dimension

        self.segmenter.clear_output()

    def scale_image(self, img_path):
        # Load image from path
        with Image.open(img_path) as image:
            width, height = image.size

            # Scale image down so that both dimensions are under MAX_IMAGE_DIMENSION
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
                
    def segment_image(self, img_path, img_num):
        self.segmenter.segment_sample(img_path, img_num)
        crops = self.segmenter.get_crops()
        return crops

    def process_image_llama(self, crops):
        # Classify the segmented images
        self.classifier.classify_imgs(crops[0])
        classifications = self.classifier.get_classifications()
        self.classifier.clear_output()

        # Generate a recipe based on the classifications
        recipe = self.recipe_generator.generate_recipe(2, classifications, "some", "some", 2, "any", "seafood")
        return recipe
    def process_images_llama(self, crops):
        self.classifier.classify_imgs(crops)
        
        classifications = self.classifier.get_classifications()
        self.classifier.clear_output()
        return classifications
        
    
    def gen_recipe(self, classifications):
        # Generate a recipe based on the classifications
        recipe = self.recipe_generator.generate_recipe(1, classifications, "some", "some", 2, "any", "none")
        return recipe

if __name__ == "__main__":
    # Initialize paths and models
    sam_model_path = "/path/to/sam_model"
    gemini_model = "gemini-2.0-flash-latest"

    # Create an instance of the driver class
    # fridge_to_recipe = FridgeToRecipe(sam_model_path, gemini_model)
    fridge_to_recipe = FridgeToRecipe(gemini_model, max_image_dimension=1000)

    # Process the image and get the recipe
    # image_path = "SeniorDesignProject/pipeline/Images/Source/refrigerator.png"
    image_paths = []
    for i in os.listdir(SOURCE_IMAGES_DIR):
        image_paths.append(SOURCE_IMAGES_DIR + i)

        # Scale image to reduce size
        fridge_to_recipe.scale_image(SOURCE_IMAGES_DIR + i)

    img_num = 1
    crops = []
    for i in os.listdir(SOURCE_IMAGES_DIR):
        crops.append(fridge_to_recipe.segment_image(SOURCE_IMAGES_DIR + i, img_num))
        img_num += 1
     
    # num = 1
    # for i in image_paths:
    #     recipe = fridge_to_recipe.process_image(i, num)
    #     num += 1
    #     print(recipe)

    
    classifications = fridge_to_recipe.process_images_llama(crops)
    recipe = fridge_to_recipe.gen_recipe(classifications)
    print(recipe)
    

    
    # Generate recipe from image
    

    # Print the recipe
    