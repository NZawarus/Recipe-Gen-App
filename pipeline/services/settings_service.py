from database.settings_databridge import SettingsDatabaseBridge
from models.settings import Settings, SettingsCreate, SettingsGet, SettingsUpdate, SettingsDelete

class SettingsService:
    def __init__(self):
        self.db = SettingsDatabaseBridge()

    def create_settings(self, user_id: int, settings: SettingsCreate):
        return self.db.create_settings(user_id, settings)

    def get_settings(self, user_id: int):
        return self.db.get_settings(user_id)
    
    def update_settings(self, user_id: int, settings: SettingsUpdate):
        return self.db.update_settings(user_id, settings)
    
    def delete_settings(self, user_id: int):
        return self.db.delete_settings(user_id) 
    
    def get_all_settings(self):
        return self.db.get_all_settings()
    
    
