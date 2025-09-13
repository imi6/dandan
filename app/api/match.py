"""Match API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.services.proxy_service import DanDanAPIProxy
from app.schemas.match import MatchRequest, MatchResponse

router = APIRouter()
proxy = DanDanAPIProxy()


@router.post("/", response_model=MatchResponse)
async def match_video(request: MatchRequest):
    """
    Match video with DanDanPlay database
    
    Args:
        request: Match request containing file info
        
    Returns:
        Match results
    """
    try:
        result = await proxy.match_video(
            file_hash=request.file_hash,
            file_name=request.file_name,
            file_size=request.file_size,
            video_duration=request.video_duration,
            match_mode=request.match_mode
        )
        
        return MatchResponse(
            success=result.get("success", False),
            is_matched=result.get("isMatched", False),
            matches=result.get("matches", []),
            error_message=result.get("errorMessage")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match failed: {str(e)}")


@router.get("/search")
async def search_anime(keyword: str):
    """
    Search anime by keyword
    
    Args:
        keyword: Search keyword
        
    Returns:
        Search results
    """
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    try:
        result = await proxy.search_anime(keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/anime/{anime_id}")
async def get_anime_detail(anime_id: int):
    """
    Get anime details
    
    Args:
        anime_id: Anime ID
        
    Returns:
        Anime details
    """
    try:
        result = await proxy.get_anime_detail(anime_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get anime details: {str(e)}")