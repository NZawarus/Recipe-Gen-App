from PIL import Image
from .main import FridgeToRecipe
import python_multipart
from fastapi import FastAPI, File, UploadFile
import io
import os
import time
import shutil
from routers import settings, recipe

app = FastAPI()

# Include routers
app.include_router(settings.router)
app.include_router(recipe.router)

# Replace These with final directory locations
SOURCE_IMAGES_DIR = "Images/uploadfile/"
SAM_MODEL_DIR = "SAM/sam2.1_hiera_large.pt"


# Initialize paths and models
gemini_model = "gemini-2.0-flash-latest"

# Create an instance of the driver class
fridge_to_recipe = FridgeToRecipe(gemini_model, max_image_dimension=1000)

# Upload an image file to the server
@app.post("/uploadfile/")
async def upload_image(file: UploadFile, user_id: int = 0):
    img_num = 0
    
    # Determine the next image id number
    if not os.path.isdir("Images/uploadfile/user" + str(user_id) + "/"):
        img_num = 1
        os.makedirs("Images/uploadfile/user" + str(user_id) + "/", exist_ok=True)
    else:
        files = os.listdir("Images/uploadfile/user" + str(user_id) + "/")
        max = 0
        for i in files:
            if i[-3:] == "png":
                if int(i[-5]) > max:
                    max = int(i[-5])
        img_num = max + 1


    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img.save("Images/uploadfile/user" + str(user_id) + "/image" + str(img_num) + ".png")
    await file.close()

    fridge_to_recipe.scale_image("Images/uploadfile/user" + str(user_id) + "/image" + str(img_num) + ".png")
    crops = fridge_to_recipe.segment_image("Images/uploadfile/user" + str(user_id) + "/image" + str(img_num) + ".png", 1)
    classifications = fridge_to_recipe.process_images_llama(crops)
    with open("Images/uploadfile/user" + str(user_id) + "/image" + str(img_num) + "classifications.txt", "w") as f:
        for i in classifications:
            f.write(i + "\n")
    return {"filename": file.filename}

# Generates a recipe using the given image file ids
@app.get("/uploadfile/")
async def get_recipe(user_id: int, file_ids):
    classifications = []
    # Get ingredients list
    for i in file_ids:
        while not os.path.exists("Images/uploadfile/user" + str(user_id) + "/image" + i + ".png"):
            sleep(1)
        with open("Images/uploadfile/user" + str(user_id) + "/image" + i + "classifications.txt", "r") as f:
            line = f.readline()
            while line:
                classifications.append(line[:-1])
                line = f.readline()
    # Generate recipe
    recipe = fridge_to_recipe.gen_recipe(classifications)
    return {"recipe": recipe}