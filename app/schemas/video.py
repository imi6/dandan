"""Video data schemas"""
from pydantic import BaseModel
from typing import Optional


class VideoInfo(BaseModel):
    """Video information"""
    id: str
    name: str
    size: int
    path: str
    url: str
    md5: Optional[str] = None
    

class VideoUploadResponse(BaseModel):
    """Video upload response"""
    success: bool
    message: str
    data: VideoInfo