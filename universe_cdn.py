"""
Universe IDE - CDN Module

Content delivery network.
"""

from typing import Any, Dict, List
import time


# ============================================================================
# ASSET
# ============================================================================

class CDNAsset:
    """CDN asset"""
    
    def __init__(self, asset_id: str, url: str, content_type: str):
        self.asset_id = asset_id
        self.url = url
        self.content_type = content_type
        self.size = 0
        self.downloads = 0
        
    def access(self):
        self.downloads += 1


# ============================================================================
# CDN
# ============================================================================

class CDN:
    """Content delivery network"""
    
    def __init__(self):
        self.assets = {}
        
    def upload(self, asset: CDNAsset):
        self.assets[asset.asset_id] = asset
        
    def get_url(self, asset_id: str) -> str:
        if asset_id in self.assets:
            self.assets[asset_id].access()
            return self.assets[asset_id].url
        return ""
        
    def list_assets(self) -> List[str]:
        return list(self.assets.keys())


# Global
_cdn = None

def get_cdn() -> CDN:
    global _cdn
    if _cdn is None:
        _cdn = CDN()
    return _cdn


__all__ = ["CDNAsset", "CDN", "get_cdn"]