"""Video API endpoints"""
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Header, Response
from fastapi.responses import StreamingResponse
from typing import Optional
import os
import re
import uuid
import aiofiles
from pathlib import Path

from app.config import settings
from app.services.md5_service import MD5Service
from app.schemas.video import VideoInfo, VideoUploadResponse

router = APIRouter()

# Store for video MD5 results (in production, use Redis or database)
video_md5_store = {}


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a video file
    
    Args:
        file: Video file to upload
        
    Returns:
        Video information and upload status
    """
    # Check file size
    if file.size and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_upload_size / (1024**3):.2f} GB"
        )
    
    # Check file type
    if not file.content_type or not file.content_type.startswith('video/'):
        # Also allow some common video extensions
        allowed_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        file_ext = Path(file.filename).suffix.lower() if file.filename else ''
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a video file."
            )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix if file.filename else '.mp4'
    file_path = os.path.join(settings.upload_dir, f"{file_id}{file_ext}")
    
    # Save file
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Prepare response
    video_info = VideoInfo(
        id=file_id,
        name=file.filename or "unknown.mp4",
        size=file_size,
        path=file_path,
        url=f"/api/video/stream/{file_id}"
    )
    
    # Calculate MD5 in background
    async def calculate_and_store_md5():
        try:
            md5_hash = await MD5Service.calculate_file_md5(file_path)
            video_md5_store[file_id] = md5_hash
        except Exception as e:
            print(f"Failed to calculate MD5: {e}")
    
    background_tasks.add_task(calculate_and_store_md5)
    
    return VideoUploadResponse(
        success=True,
        message="Video uploaded successfully",
        data=video_info
    )


@router.get("/md5/{video_id}")
async def get_video_md5(video_id: str):
    """
    Get MD5 hash of a video
    
    Args:
        video_id: Video ID
        
    Returns:
        MD5 hash if available
    """
    md5_hash = video_md5_store.get(video_id)
    
    if md5_hash:
        return {"md5": md5_hash, "ready": True}
    else:
        # Try to calculate if file exists
        video_files = list(Path(settings.upload_dir).glob(f"{video_id}.*"))
        if video_files:
            try:
                md5_hash = await MD5Service.calculate_file_md5(str(video_files[0]))
                video_md5_store[video_id] = md5_hash
                return {"md5": md5_hash, "ready": True}
            except Exception as e:
                return {"md5": None, "ready": False, "error": str(e)}
        
        return {"md5": None, "ready": False}


@router.get("/stream/{video_id}")
async def stream_video(
    video_id: str,
    range: Optional[str] = Header(None)
):
    """
    Stream video with range support
    
    Args:
        video_id: Video ID
        range: Range header for partial content
        
    Returns:
        Video stream
    """
    # Find video file
    video_files = list(Path(settings.upload_dir).glob(f"{video_id}.*"))
    if not video_files:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_path = str(video_files[0])
    video_size = os.path.getsize(video_path)
    
    # Parse range header
    start = 0
    end = video_size - 1
    
    if range:
        match = re.search(r'bytes=(\d+)-(\d*)', range)
        if match:
            start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
    
    # Create streaming response
    async def iterfile():
        async with aiofiles.open(video_path, 'rb') as f:
            await f.seek(start)
            chunk_size = 1024 * 1024  # 1MB chunks
            current = start
            
            while current <= end:
                read_size = min(chunk_size, end - current + 1)
                data = await f.read(read_size)
                if not data:
                    break
                current += len(data)
                yield data
    
    # Determine content type
    file_ext = Path(video_path).suffix.lower()
    content_types = {
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.mkv': 'video/x-matroska',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime',
        '.wmv': 'video/x-ms-wmv',
        '.flv': 'video/x-flv'
    }
    content_type = content_types.get(file_ext, 'video/mp4')
    
    headers = {
        'Content-Range': f'bytes {start}-{end}/{video_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(end - start + 1),
        'Content-Type': content_type,
    }
    
    return StreamingResponse(
        iterfile(),
        status_code=206 if range else 200,
        headers=headers
    )


@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """
    Delete a video file
    
    Args:
        video_id: Video ID
        
    Returns:
        Deletion status
    """
    video_files = list(Path(settings.upload_dir).glob(f"{video_id}.*"))
    
    if not video_files:
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        for file_path in video_files:
            file_path.unlink()
        
        # Remove from MD5 store
        video_md5_store.pop(video_id, None)
        
        return {"success": True, "message": "Video deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete video: {str(e)}")