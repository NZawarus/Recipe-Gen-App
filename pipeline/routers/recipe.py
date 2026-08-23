from fastapi import APIRouter, HTTPException
from models.recipes import Recipe, RecipeCreate, RecipeGet, RecipeUpdate, RecipeDelete
from services.recipe_service import RecipeService

router = APIRouter()

@router.post("/recipes")
async def create_recipe(recipe: RecipeCreate) -> Recipe:
    return RecipeService().create_recipe(recipe)

@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int) -> Recipe:
    return RecipeService().get_recipe(recipe_id)

@router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: RecipeUpdate) -> Recipe:
    return RecipeService().update_recipe(recipe_id, recipe)

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int) -> Recipe:
    return RecipeService().delete_recipe(recipe_id)

@router.get("/recipes")
async def get_all_recipes(user_id: int) -> list[Recipe]:
    return RecipeService().get_all_recipes(user_id)


