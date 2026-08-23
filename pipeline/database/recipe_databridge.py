import pymysql
from models.recipes import Recipe, RecipeCreate, RecipeGet, RecipeUpdate, RecipeDelete

class RecipeDatabaseBridge:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1517109mysql-', db='food_users')
        self.cursor = self.conn.cursor()

    def create_recipe(self, recipe: RecipeCreate):
        self.cursor.execute(
            """INSERT INTO recipes (name, description, ingredients, instructions)
               VALUES (%s, %s, %s, %s)""",
            (recipe.name, recipe.description, recipe.ingredients, recipe.instructions)
        )
        self.conn.commit()

    def get_recipe(self, recipe_id: int):
        self.cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
        return self.cursor.fetchone()
    
    def update_recipe(self, recipe_id: int, recipe: RecipeUpdate):
        self.cursor.execute(
            """UPDATE recipes SET name = %s, description = %s, ingredients = %s, instructions = %s WHERE id = %s""",
            (recipe.name, recipe.description, recipe.ingredients, recipe.instructions, recipe_id)
        )
        self.conn.commit()

    def delete_recipe(self, recipe_id: int):
        self.cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
        self.conn.commit()

    def get_all_recipes(self, user_id: int):
        self.cursor.execute("SELECT * FROM recipes WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()
    
    
        
