"""Danmaku data schemas"""
from pydantic import BaseModel
from typing import List, Any, Dict


class DanmakuResponse(BaseModel):
    """Danmaku response"""
    success: bool
    count: int
    comments: List[Dict[str, Any]]


class ConvertRequest(BaseModel):
    """Danmaku format conversion request"""
    comments: List[Dict[str, Any]]
    target_format: str  # nplayer, artplayer, ccl


class XMLParseRequest(BaseModel):
    """XML danmaku parse request"""
    xml_content: str