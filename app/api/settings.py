"""Settings API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
import os
from pathlib import Path

from app.config import settings as app_settings

router = APIRouter()

# Settings file path
SETTINGS_FILE = Path("user_settings.json")


@router.get("/")
async def get_settings():
    """
    Get user settings
    
    Returns:
        User settings object
    """
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    # Return default settings
    return get_default_settings()


@router.post("/")
async def save_settings(settings: Dict[str, Any]):
    """
    Save user settings
    
    Args:
        settings: Settings object to save
        
    Returns:
        Success status
    """
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        # Apply some settings immediately
        apply_settings(settings)
        
        return {"success": True, "message": "Settings saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save settings: {str(e)}")


@router.delete("/")
async def reset_settings():
    """
    Reset settings to default
    
    Returns:
        Default settings
    """
    try:
        if SETTINGS_FILE.exists():
            os.remove(SETTINGS_FILE)
        return {"success": True, "settings": get_default_settings()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset settings: {str(e)}")


def get_default_settings() -> Dict[str, Any]:
    """Get default settings"""
    return {
        "general": {
            "theme": "auto",           # auto, light, dark
            "language": "zh-CN",       # zh-CN, zh-TW, en, ja
            "autoMatch": True,         # 自动匹配弹幕
            "saveHistory": True        # 保存播放历史
        },
        "player": {
            "engine": "native",        # native, nplayer, artplayer, dplayer
            "defaultVolume": 80,       # 0-100
            "autoPlay": False,         # 自动播放
            "rememberPosition": True   # 记忆播放位置
        },
        "danmaku": {
            "opacity": 100,            # 0-100 透明度
            "fontSize": "medium",      # small, medium, large, xlarge
            "speed": "normal",         # slow, normal, fast
            "blockTop": False,         # 屏蔽顶部弹幕
            "blockBottom": False,      # 屏蔽底部弹幕
            "blockScroll": False,      # 屏蔽滚动弹幕
            "smartBlock": False        # 智能防挡
        },
        "network": {
            "apiServer": str(app_settings.dandan_api_base_url),
            "useProxy": bool(app_settings.dandan_proxy_url),
            "proxyUrl": str(app_settings.dandan_proxy_url) if app_settings.dandan_proxy_url else "",
            "enableCache": True,
            "cacheExpiry": 86400      # 缓存过期时间(秒)
        },
        "advanced": {
            "hardwareAcceleration": True,
            "debugMode": False,
            "logLevel": "info",       # debug, info, warning, error
            "maxUploadSize": 500      # MB
        }
    }


def apply_settings(settings: Dict[str, Any]):
    """Apply settings that need immediate effect"""
    # Apply settings that affect the server
    
    if "advanced" in settings:
        if "maxUploadSize" in settings["advanced"]:
            # Convert MB to bytes
            new_limit = settings["advanced"]["maxUploadSize"] * 1024 * 1024
            app_settings.max_upload_size = new_limit
        
        if "debugMode" in settings["advanced"]:
            app_settings.debug = settings["advanced"]["debugMode"]
    
    if "network" in settings:
        if "apiServer" in settings["network"]:
            app_settings.dandan_api_base_url = settings["network"]["apiServer"]
        if "proxyUrl" in settings["network"]:
            app_settings.dandan_proxy_url = settings["network"]["proxyUrl"] or None
        if "useProxy" in settings["network"]:
            if not settings["network"]["useProxy"]:
                app_settings.dandan_proxy_url = None
