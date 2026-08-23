import pymysql
from models.settings import Settings, SettingsCreate, SettingsGet, SettingsUpdate, SettingsDelete
from models.settings import Preferences, NutritionalPreferences, Allergens, DietaryPreferences

class SettingsDatabaseBridge:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1517109mysql-', db='food_users')
        self.cursor = self.conn.cursor()

    def create_settings(self, user_id: int, settings: SettingsCreate):
        # Create preferences
        self.cursor.execute(
            """INSERT INTO UserPreferences (user_id, theme, notifications_enabled)
               VALUES (%s, %s, %s)""",
            (user_id, settings.preferences.theme, settings.preferences.notifications_enabled)
        )
        
        # Create nutritional preferences
        self.cursor.execute(
            """INSERT INTO NutritionalPreferences 
               (user_id, protein, fat, carbs, sodium, sugars, calories)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_id, settings.nutritional_preferences.protein, settings.nutritional_preferences.fat,
             settings.nutritional_preferences.carbs, settings.nutritional_preferences.sodium,
             settings.nutritional_preferences.sugars, settings.nutritional_preferences.calories)
        )
        
        # Create allergens
        self.cursor.execute(
            """INSERT INTO Allergens (user_id, allergen_name)
               VALUES (%s, %s)""",
            (user_id, settings.allergens.allergen_name)
        )
        
        # Create dietary preferences
        self.cursor.execute(
            """INSERT INTO DietaryPreferences (user_id, diet_type, custom_description)
               VALUES (%s, %s, %s)""",
            (user_id, settings.dietary_preferences.diet_type, 
             settings.dietary_preferences.custom_description)
        )
        
        self.conn.commit()
        return user_id

    def get_settings(self, user_id: int):
        # Get preferences
        self.cursor.execute("SELECT * FROM UserPreferences WHERE user_id = %s", (user_id,))
        preferences_data = self.cursor.fetchone()
        preferences = Preferences(
            user_id=preferences_data[0],
            theme=preferences_data[1],
            notifications_enabled=preferences_data[2]
        ) if preferences_data else None
        
        # Get nutritional preferences
        self.cursor.execute("SELECT * FROM NutritionalPreferences WHERE user_id = %s", (user_id,))
        nutritional_data = self.cursor.fetchone()
        nutritional_preferences = NutritionalPreferences(
            user_id=nutritional_data[0],
            protein=nutritional_data[1],
            fat=nutritional_data[2],
            carbs=nutritional_data[3],
            sodium=nutritional_data[4],
            sugars=nutritional_data[5],
            calories=nutritional_data[6]
        ) if nutritional_data else None
        
        # Get allergens
        self.cursor.execute("SELECT * FROM Allergens WHERE user_id = %s", (user_id,))
        allergens_data = self.cursor.fetchone()
        allergens = Allergens(
            allergen_id=allergens_data[0],
            user_id=allergens_data[1],
            allergen_name=allergens_data[2]
        ) if allergens_data else None
        
        # Get dietary preferences
        self.cursor.execute("SELECT * FROM DietaryPreferences WHERE user_id = %s", (user_id,))
        dietary_data = self.cursor.fetchone()
        dietary_preferences = DietaryPreferences(
            user_id=dietary_data[0],
            diet_type=dietary_data[1],
            custom_description=dietary_data[2]
        ) if dietary_data else None
        
        # Create and return complete settings object
        if preferences and nutritional_preferences and allergens and dietary_preferences:
            return Settings(
                user_id=user_id,
                preferences=preferences,
                nutritional_preferences=nutritional_preferences,
                allergens=allergens,
                dietary_preferences=dietary_preferences
            )
        return None

    def update_settings(self, user_id: int, settings: SettingsUpdate):
        # Update preferences if provided
        if settings.preferences:
            update_fields = []
            update_values = []
            
            if settings.preferences.theme is not None:
                update_fields.append("theme = %s")
                update_values.append(settings.preferences.theme)
                
            if settings.preferences.notification is not None:
                update_fields.append("notification = %s")
                update_values.append(settings.preferences.notification)
                
            if update_fields:
                query = f"UPDATE UserPreferences SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                self.cursor.execute(query, tuple(update_values))
        
        # Update nutritional preferences if provided
        if settings.nutritional_preferences:
            update_fields = []
            update_values = []
            
            if settings.nutritional_preferences.protein is not None:
                update_fields.append("protein = %s")
                update_values.append(settings.nutritional_preferences.protein)
                
            if settings.nutritional_preferences.fat is not None:
                update_fields.append("fat = %s")
                update_values.append(settings.nutritional_preferences.fat)
                
            if settings.nutritional_preferences.carbs is not None:
                update_fields.append("carbs = %s")
                update_values.append(settings.nutritional_preferences.carbs)
                
            if settings.nutritional_preferences.sodium is not None:
                update_fields.append("sodium = %s")
                update_values.append(settings.nutritional_preferences.sodium)
                
            if settings.nutritional_preferences.sugars is not None:
                update_fields.append("sugars = %s")
                update_values.append(settings.nutritional_preferences.sugars)
                
            if settings.nutritional_preferences.calories is not None:
                update_fields.append("calories = %s")
                update_values.append(settings.nutritional_preferences.calories)
                
            if update_fields:
                query = f"UPDATE NutritionalPreferences SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                self.cursor.execute(query, tuple(update_values))
        
        # Update allergens if provided
        if settings.allergens and settings.allergens.allergen_name is not None:
            self.cursor.execute(
                "UPDATE Allergens SET allergen_name = %s WHERE user_id = %s",
                (settings.allergens.allergen_name, user_id)
            )
        
        # Update dietary preferences if provided
        if settings.dietary_preferences:
            update_fields = []
            update_values = []
            
            if settings.dietary_preferences.diet_type is not None:
                update_fields.append("diet_type = %s")
                update_values.append(settings.dietary_preferences.diet_type)
                
            if settings.dietary_preferences.custom_description is not None:
                update_fields.append("custom_description = %s")
                update_values.append(settings.dietary_preferences.custom_description)
                
            if update_fields:
                query = f"UPDATE DietaryPreferences SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                self.cursor.execute(query, tuple(update_values))
        
        self.conn.commit()
        return user_id

    def delete_settings(self, user_id: int):
        # Delete all settings related to user
        self.cursor.execute("DELETE FROM UserPreferences WHERE user_id = %s", (user_id,))
        self.cursor.execute("DELETE FROM NutritionalPreferences WHERE user_id = %s", (user_id,))
        self.cursor.execute("DELETE FROM Allergens WHERE user_id = %s", (user_id,))
        self.cursor.execute("DELETE FROM DietaryPreferences WHERE user_id = %s", (user_id,))
        self.conn.commit()
        return user_id

