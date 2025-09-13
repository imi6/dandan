"""Match data schemas"""
from pydantic import BaseModel
from typing import Optional, List


class MatchRequest(BaseModel):
    """Video match request"""
    file_name: str
    file_hash: str
    file_size: int
    video_duration: Optional[int] = None
    match_mode: Optional[str] = None


class MatchInfo(BaseModel):
    """Single match result"""
    episode_id: int
    anime_id: int
    anime_title: str
    episode_title: str
    type: str
    type_description: str
    shift: float


class MatchResponse(BaseModel):
    """Match response"""
    success: bool
    is_matched: bool
    matches: List[MatchInfo]
    error_message: Optional[str] = None