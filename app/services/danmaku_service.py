"""Danmaku (comment) processing service"""
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError


class DanmakuConverter:
    """Service for converting danmaku between different formats"""
    
    @staticmethod
    def dandan_to_nplayer(raw_comment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert DanDanPlay format to NPlayer format
        
        Args:
            raw_comment: DanDanPlay comment format
                {
                    "cid": int,
                    "p": "time,mode,color",
                    "m": "text"
                }
                
        Returns:
            NPlayer comment format
        """
        try:
            params = raw_comment["p"].split(",")
            time = float(params[0])
            mode = params[1]
            color = int(params[2])
            
            # Mode mapping
            mode_map = {
                "1": "scroll",  # Rolling
                "4": "bottom",  # Bottom
                "5": "top"      # Top
            }
            
            return {
                "color": f"#{color:06x}",
                "text": raw_comment["m"],
                "time": time,
                "type": mode_map.get(mode, "scroll")
            }
        except (KeyError, IndexError, ValueError) as e:
            raise ValueError(f"Invalid comment format: {e}")
    
    @staticmethod
    def dandan_to_artplayer(raw_comment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert DanDanPlay format to ArtPlayer format
        
        Args:
            raw_comment: DanDanPlay comment format
            
        Returns:
            ArtPlayer comment format
        """
        try:
            params = raw_comment["p"].split(",")
            time = float(params[0])
            mode = params[1]
            color = int(params[2])
            
            # Mode mapping (ArtPlayer uses 0 for scroll, 1 for static)
            mode_map = {
                "1": 0,  # Rolling
                "4": 1,  # Bottom (static)
                "5": 1   # Top (static)
            }
            
            return {
                "text": raw_comment["m"],
                "time": time,
                "color": f"#{color:06x}",
                "mode": mode_map.get(mode, 0)
            }
        except (KeyError, IndexError, ValueError) as e:
            raise ValueError(f"Invalid comment format: {e}")
    
    @staticmethod
    def dandan_to_ccl(raw_comment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert DanDanPlay format to CCL (Comment Core Library) format
        
        Args:
            raw_comment: DanDanPlay comment format
            
        Returns:
            CCL comment format
        """
        try:
            params = raw_comment["p"].split(",")
            time = float(params[0])
            mode = int(params[1])
            color = int(params[2])
            
            return {
                "text": raw_comment["m"],
                "stime": int(time * 1000),  # CCL uses milliseconds
                "color": color,
                "mode": mode,
                "size": 25  # Default size
            }
        except (KeyError, IndexError, ValueError) as e:
            raise ValueError(f"Invalid comment format: {e}")
    
    @staticmethod
    def parse_bilibili_xml(xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse Bilibili XML danmaku format
        
        Args:
            xml_content: XML string containing Bilibili danmaku
            
        Returns:
            List of comments in DanDanPlay format
        """
        try:
            root = ET.fromstring(xml_content)
            comments = []
            
            for idx, d_elem in enumerate(root.findall('d')):
                p_attr = d_elem.get('p', '')
                text = d_elem.text or ''
                
                if not p_attr or not text:
                    continue
                
                # Bilibili format: time,mode,size,color,timestamp,pool,userid,dmid
                p_parts = p_attr.split(',')
                if len(p_parts) >= 4:
                    # Convert to DanDanPlay format: time,mode,color
                    time = p_parts[0]
                    mode = p_parts[1]
                    color = p_parts[3]
                    
                    comments.append({
                        "cid": idx,
                        "p": f"{time},{mode},{color}",
                        "m": text.strip()
                    })
            
            return comments
            
        except (ET.ParseError, ExpatError) as e:
            raise ValueError(f"Failed to parse XML: {e}")
    
    @staticmethod
    def convert_batch(
        comments: List[Dict[str, Any]],
        target_format: str = "nplayer"
    ) -> List[Dict[str, Any]]:
        """
        Convert a batch of comments to target format
        
        Args:
            comments: List of comments in DanDanPlay format
            target_format: Target format (nplayer, artplayer, ccl)
            
        Returns:
            List of converted comments
        """
        converters = {
            "nplayer": DanmakuConverter.dandan_to_nplayer,
            "artplayer": DanmakuConverter.dandan_to_artplayer,
            "ccl": DanmakuConverter.dandan_to_ccl
        }
        
        converter = converters.get(target_format)
        if not converter:
            raise ValueError(f"Unsupported format: {target_format}")
        
        converted = []
        for comment in comments:
            try:
                converted.append(converter(comment))
            except ValueError:
                # Skip invalid comments
                continue
        
        return converted