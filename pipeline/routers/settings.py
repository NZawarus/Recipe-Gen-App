from fastapi import APIRouter, HTTPException
from models.settings import Settings, SettingsCreate, SettingsGet, SettingsUpdate, SettingsDelete
from services.settings_service import SettingsService

router = APIRouter()

@router.post("/settings/{user_id}")
async def create_settings(user_id: int, settings: SettingsCreate):
    """Create settings for a user"""
    return SettingsService().create_settings(user_id, settings)

@router.get("/settings/{user_id}")
async def get_settings(user_id: int):
    """Get settings for a user"""
    settings = SettingsService().get_settings(user_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/settings/{user_id}")
async def update_settings(user_id: int, settings: SettingsUpdate):
    """Update settings for a user"""
    result = SettingsService().update_settings(user_id, settings)
    if not result:
        raise HTTPException(status_code=404, detail="Settings not found")
    return {"status": "Settings updated successfully"}

@router.delete("/settings/{user_id}")
async def delete_settings(user_id: int):
    """Delete settings for a user"""
    result = SettingsService().delete_settings(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Settings not found")
    return {"status": "Settings deleted successfully"} 