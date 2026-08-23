from pydantic import BaseModel
from datetime import datetime

class Recipe(BaseModel):
    user_id: int
    recipe_name: str
    recipe_content: str

class RecipeCreate(BaseModel):
    recipe_name: str
    recipe_content: str

class RecipeGet(BaseModel):
    recipe_id: int | None = None
    recipe_name: str | None = None
    recipe_content: str | None = None

class RecipeUpdate(BaseModel):
    recipe_name: str | None = None
    recipe_content: str | None = None

class RecipeDelete(BaseModel):
    recipe_id: int