"""Danmaku (comment) API endpoints"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from app.services.proxy_service import DanDanAPIProxy
from app.services.danmaku_service import DanmakuConverter
from app.schemas.danmaku import (
    DanmakuResponse,
    ConvertRequest,
    XMLParseRequest
)

router = APIRouter()
proxy = DanDanAPIProxy()


@router.get("/{episode_id}")
async def get_danmaku(
    episode_id: int,
    format: str = Query("raw", description="Output format: raw, nplayer, artplayer, ccl"),
    with_related: bool = Query(True, description="Include related comments"),
    ch_convert: Optional[int] = Query(None, description="Chinese conversion: 0=none, 1=simplified, 2=traditional")
):
    """
    Get danmaku for an episode
    
    Args:
        episode_id: Episode ID from match result
        format: Output format
        with_related: Include related comments
        ch_convert: Chinese conversion option
        
    Returns:
        Danmaku data
    """
    try:
        result = await proxy.get_comments(
            episode_id=episode_id,
            with_related=with_related,
            ch_convert=ch_convert
        )
        
        if not result.get("success", False):
            error_msg = result.get("errorMessage", "Failed to get comments")
            raise HTTPException(status_code=400, detail=error_msg)
        
        comments = result.get("comments", [])
        count = result.get("count", 0)
        
        # Convert format if requested
        if format != "raw" and comments:
            try:
                comments = DanmakuConverter.convert_batch(comments, format)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid format: {str(e)}")
        
        return DanmakuResponse(
            success=True,
            count=count,
            comments=comments
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get danmaku: {str(e)}")


@router.post("/external")
async def get_external_danmaku(
    url: str,
    format: str = Query("raw", description="Output format: raw, nplayer, artplayer, ccl")
):
    """
    Get danmaku from external sources (Bilibili, AcFun, etc.)
    
    Args:
        url: URL of the external video
        format: Output format
        
    Returns:
        Danmaku data
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        result = await proxy.get_extcomment(url)
        
        if not result.get("success", False):
            error_msg = result.get("errorMessage", "Failed to get external comments")
            raise HTTPException(status_code=400, detail=error_msg)
        
        comments = result.get("comments", [])
        count = result.get("count", 0)
        
        # Convert format if requested
        if format != "raw" and comments:
            try:
                comments = DanmakuConverter.convert_batch(comments, format)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid format: {str(e)}")
        
        return DanmakuResponse(
            success=True,
            count=count,
            comments=comments
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get external danmaku: {str(e)}")


@router.post("/parse/xml")
async def parse_xml_danmaku(
    request: XMLParseRequest,
    format: str = Query("raw", description="Output format: raw, nplayer, artplayer, ccl")
):
    """
    Parse XML danmaku (Bilibili format)
    
    Args:
        request: XML content to parse
        format: Output format
        
    Returns:
        Parsed danmaku data
    """
    try:
        comments = DanmakuConverter.parse_bilibili_xml(request.xml_content)
        count = len(comments)
        
        # Convert format if requested
        if format != "raw" and comments:
            try:
                comments = DanmakuConverter.convert_batch(comments, format)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid format: {str(e)}")
        
        return DanmakuResponse(
            success=True,
            count=count,
            comments=comments
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse XML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/convert")
async def convert_danmaku(request: ConvertRequest):
    """
    Convert danmaku format
    
    Args:
        request: Danmaku data and target format
        
    Returns:
        Converted danmaku
    """
    try:
        converted = DanmakuConverter.convert_batch(
            request.comments,
            request.target_format
        )
        
        return {
            "success": True,
            "count": len(converted),
            "comments": converted
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")