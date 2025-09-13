"""DanDanPlay API proxy service"""
import httpx
from typing import Dict, List, Optional
from app.config import settings


class DanDanAPIProxy:
    """Proxy service for DanDanPlay API"""
    
    def __init__(self):
        self.base_url = settings.dandan_proxy_url or settings.dandan_api_base_url
        self.timeout = httpx.Timeout(30.0, connect=10.0)
    
    async def match_video(
        self,
        file_hash: str,
        file_name: str,
        file_size: int,
        video_duration: Optional[int] = None,
        match_mode: Optional[str] = None
    ) -> Dict:
        """
        Match video with DanDanPlay database
        
        Args:
            file_hash: MD5 hash of video file (first 16MB)
            file_name: Name of the video file
            file_size: Size of the video file in bytes
            video_duration: Duration of video in seconds (optional)
            match_mode: Match mode (optional)
            
        Returns:
            Match result from API
        """
        payload = {
            "fileName": file_name,
            "fileHash": file_hash,
            "fileSize": file_size
        }
        
        if video_duration:
            payload["videoDuration"] = video_duration
        if match_mode:
            payload["matchMode"] = match_mode
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/match",
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def get_comments(
        self,
        episode_id: int,
        from_source: Optional[str] = None,
        with_related: bool = True,
        ch_convert: Optional[int] = None
    ) -> Dict:
        """
        Get comments (danmaku) for an episode
        
        Args:
            episode_id: Episode ID from match result
            from_source: Source filter (optional)
            with_related: Include related comments
            ch_convert: Chinese conversion (0: none, 1: to simplified, 2: to traditional)
            
        Returns:
            Comments data from API
        """
        params = {}
        
        if from_source:
            params["from"] = from_source
        if with_related:
            params["withRelated"] = "true"
        if ch_convert is not None:
            params["chConvert"] = str(ch_convert)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/comment/{episode_id}",
                params=params
            )
            response.raise_for_status()
            return response.json()
    
    async def get_extcomment(self, url: str) -> Dict:
        """
        Get comments from third-party sources (Bilibili, AcFun, etc.)
        
        Args:
            url: URL of the third-party video
            
        Returns:
            Comments data from API
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/extcomment",
                params={"url": url}
            )
            response.raise_for_status()
            return response.json()
    
    async def search_anime(self, keyword: str) -> Dict:
        """
        Search anime by keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            Search results from API
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/search/anime",
                params={"keyword": keyword}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_anime_detail(self, anime_id: int) -> Dict:
        """
        Get anime details
        
        Args:
            anime_id: Anime ID
            
        Returns:
            Anime details from API
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/anime/{anime_id}"
            )
            response.raise_for_status()
            return response.json()