"""MD5 calculation service"""
import hashlib
import aiofiles
from pathlib import Path


class MD5Service:
    """Service for calculating MD5 hash of video files"""
    
    @staticmethod
    async def calculate_file_md5(file_path: str, chunk_size: int = 16 * 1024 * 1024) -> str:
        """
        Calculate MD5 hash of the first 16MB of a file (DanDanPlay standard)
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunk to read (default 16MB)
            
        Returns:
            MD5 hash as hex string
        """
        md5_hash = hashlib.md5()
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        async with aiofiles.open(file_path, 'rb') as f:
            # Read only the first chunk (16MB) as per DanDanPlay specification
            chunk = await f.read(chunk_size)
            md5_hash.update(chunk)
        
        return md5_hash.hexdigest()
    
    @staticmethod
    def calculate_md5_sync(file_path: str, chunk_size: int = 16 * 1024 * 1024) -> str:
        """
        Synchronous version of MD5 calculation
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunk to read (default 16MB)
            
        Returns:
            MD5 hash as hex string
        """
        md5_hash = hashlib.md5()
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            # Read only the first chunk (16MB)
            chunk = f.read(chunk_size)
            md5_hash.update(chunk)
        
        return md5_hash.hexdigest()