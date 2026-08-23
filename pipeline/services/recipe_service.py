from database.recipe_databridge import RecipeDatabaseBridge
from models.recipes import Recipe, RecipeCreate, RecipeGet, RecipeUpdate, RecipeDelete

class RecipeService:
    def __init__(self):
        self.db = RecipeDatabaseBridge()

    def create_recipe(self, recipe: RecipeCreate):
        return self.db.create_recipe(recipe)

    def get_recipe(self, recipe_id: int):
        return self.db.get_recipe(recipe_id)
    
    def update_recipe(self, recipe_id: int, recipe: RecipeUpdate):
        return self.db.update_recipe(recipe_id, recipe)
    
    def delete_recipe(self, recipe_id: int):
        return self.db.delete_recipe(recipe_id)
    
    def get_all_recipes(self, user_id: int):
        return self.db.get_all_recipes(user_id)
    
    
