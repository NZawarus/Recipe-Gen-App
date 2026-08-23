from pydantic import BaseModel

class Preferences(BaseModel):
    user_id: int
    theme: str
    notifications_enabled: bool

class PreferencesCreate(BaseModel):
    theme: str
    notifications_enabled: bool

class PreferencesGet(BaseModel):
    theme: str | None = None
    notifications_enabled: bool | None = None

class PreferencesUpdate(BaseModel):
    theme: str | None = None
    notifications_enabled: bool | None = None

class PreferencesDelete(BaseModel):
    user_id: int

class NutritionalPreferences(BaseModel):
    user_id: int
    protein: float
    fat: float
    carbs: float
    sodium: float
    sugars: float
    calories: float

class NutritionalPreferencesCreate(BaseModel):
    protein: float
    fat: float
    carbs: float
    sodium: float
    sugars: float
    calories: float

class NutritionalPreferencesGet(BaseModel):
    protein: float | None = None
    fat: float | None = None
    carbs: float | None = None
    sodium: float | None = None
    sugars: float | None = None
    calories: float | None = None

class NutritionalPreferencesUpdate(BaseModel):
    protein: float | None = None
    fat: float | None = None
    carbs: float | None = None
    sodium: float | None = None
    sugars: float | None = None
    calories: float | None = None

class NutritionalPreferencesDelete(BaseModel):
    user_id: int

class Allergens(BaseModel):
    allergen_id: int
    user_id: int
    allergen_name: str

class AllergensCreate(BaseModel):
    allergen_name: str

class AllergensGet(BaseModel):
    allergen_name: str | None = None

class AllergensUpdate(BaseModel):
    allergen_name: str | None = None

class AllergensDelete(BaseModel):
    allergen_id: int

class DietaryPreferences(BaseModel):
    user_id: int
    diet_type: str
    custom_description: str

class DietaryPreferencesCreate(BaseModel):
    diet_type: str
    custom_description: str

class DietaryPreferencesGet(BaseModel):
    diet_type: str | None = None
    custom_description: str | None = None

class DietaryPreferencesUpdate(BaseModel):
    diet_type: str | None = None
    custom_description: str | None = None

class DietaryPreferencesDelete(BaseModel):
    user_id: int

class Settings(BaseModel):
    user_id: int
    preferences: Preferences
    nutritional_preferences: NutritionalPreferences
    allergens: Allergens
    dietary_preferences: DietaryPreferences

class SettingsCreate(BaseModel):
    preferences: PreferencesCreate
    nutritional_preferences: NutritionalPreferencesCreate
    allergens: AllergensCreate
    dietary_preferences: DietaryPreferencesCreate

class SettingsGet(BaseModel):
    preferences: PreferencesGet
    nutritional_preferences: NutritionalPreferencesGet
    allergens: AllergensGet
    dietary_preferences: DietaryPreferencesGet

class SettingsUpdate(BaseModel):
    preferences: PreferencesUpdate
    nutritional_preferences: NutritionalPreferencesUpdate
    allergens: AllergensUpdate
    dietary_preferences: DietaryPreferencesUpdate

class SettingsDelete(BaseModel):
    user_id: int
