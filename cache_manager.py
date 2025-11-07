"""
Cache Manager Module
Provides intelligent caching for API responses to reduce quota usage and improve performance
"""

import os
import json
import hashlib
import time
from typing import Optional, Dict, Any
from pathlib import Path


class CacheManager:
    """Manages caching of API responses with TTL support"""
    
    def __init__(self, cache_dir: str = '.cache', default_ttl: int = 3600):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different cache types
        self.video_cache_dir = self.cache_dir / 'videos'
        self.comments_cache_dir = self.cache_dir / 'comments'
        self.search_cache_dir = self.cache_dir / 'searches'
        
        for cache_subdir in [self.video_cache_dir, self.comments_cache_dir, self.search_cache_dir]:
            cache_subdir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, identifier: str) -> str:
        """Generate a cache key hash from an identifier"""
        return hashlib.md5(identifier.encode()).hexdigest()
    
    def _get_cache_path(self, cache_type: str, identifier: str) -> Path:
        """Get the file path for a cached item"""
        cache_key = self._get_cache_key(identifier)
        
        if cache_type == 'video':
            return self.video_cache_dir / f"{cache_key}.json"
        elif cache_type == 'comments':
            return self.comments_cache_dir / f"{cache_key}.json"
        elif cache_type == 'search':
            return self.search_cache_dir / f"{cache_key}.json"
        else:
            raise ValueError(f"Unknown cache type: {cache_type}")
    
    def get(self, cache_type: str, identifier: str) -> Optional[Any]:
        """
        Retrieve cached data if available and not expired
        
        Args:
            cache_type: Type of cache ('video', 'comments', 'search')
            identifier: Unique identifier for the cached item
            
        Returns:
            Cached data if available and valid, None otherwise
        """
        cache_path = self._get_cache_path(cache_type, identifier)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache has expired
            cached_at = cache_data.get('cached_at', 0)
            ttl = cache_data.get('ttl', self.default_ttl)
            
            if time.time() - cached_at > ttl:
                # Cache expired, remove it
                cache_path.unlink()
                return None
            
            return cache_data.get('data')
            
        except (json.JSONDecodeError, IOError):
            # Invalid cache file, remove it
            if cache_path.exists():
                cache_path.unlink()
            return None
    
    def set(self, cache_type: str, identifier: str, data: Any, ttl: Optional[int] = None) -> bool:
        """
        Store data in cache
        
        Args:
            cache_type: Type of cache ('video', 'comments', 'search')
            identifier: Unique identifier for the cached item
            data: Data to cache
            ttl: Time-to-live in seconds (uses default if not specified)
            
        Returns:
            True if successfully cached, False otherwise
        """
        cache_path = self._get_cache_path(cache_type, identifier)
        
        cache_data = {
            'cached_at': time.time(),
            'ttl': ttl or self.default_ttl,
            'identifier': identifier,
            'data': data
        }
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def invalidate(self, cache_type: str, identifier: str) -> bool:
        """
        Remove a specific cached item
        
        Args:
            cache_type: Type of cache ('video', 'comments', 'search')
            identifier: Unique identifier for the cached item
            
        Returns:
            True if cache was removed, False if it didn't exist
        """
        cache_path = self._get_cache_path(cache_type, identifier)
        
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    
    def clear(self, cache_type: Optional[str] = None) -> int:
        """
        Clear all cached items of a specific type or all caches
        
        Args:
            cache_type: Type of cache to clear ('video', 'comments', 'search'), or None for all
            
        Returns:
            Number of cache files removed
        """
        count = 0
        
        if cache_type is None:
            # Clear all caches
            for subdir in [self.video_cache_dir, self.comments_cache_dir, self.search_cache_dir]:
                for cache_file in subdir.glob('*.json'):
                    cache_file.unlink()
                    count += 1
        else:
            # Clear specific cache type
            if cache_type == 'video':
                cache_subdir = self.video_cache_dir
            elif cache_type == 'comments':
                cache_subdir = self.comments_cache_dir
            elif cache_type == 'search':
                cache_subdir = self.search_cache_dir
            else:
                return 0
            
            for cache_file in cache_subdir.glob('*.json'):
                cache_file.unlink()
                count += 1
        
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        def get_dir_stats(cache_dir: Path) -> Dict[str, int]:
            """Get statistics for a cache directory"""
            files = list(cache_dir.glob('*.json'))
            valid_count = 0
            expired_count = 0
            total_size = 0
            
            for cache_file in files:
                total_size += cache_file.stat().st_size
                
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_at = cache_data.get('cached_at', 0)
                    ttl = cache_data.get('ttl', self.default_ttl)
                    
                    if time.time() - cached_at > ttl:
                        expired_count += 1
                    else:
                        valid_count += 1
                except (json.JSONDecodeError, IOError, OSError, KeyError):
                    expired_count += 1
            
            return {
                'total': len(files),
                'valid': valid_count,
                'expired': expired_count,
                'size_bytes': total_size
            }
        
        video_stats = get_dir_stats(self.video_cache_dir)
        comments_stats = get_dir_stats(self.comments_cache_dir)
        search_stats = get_dir_stats(self.search_cache_dir)
        
        total_size = video_stats['size_bytes'] + comments_stats['size_bytes'] + search_stats['size_bytes']
        
        return {
            'video': video_stats,
            'comments': comments_stats,
            'search': search_stats,
            'total_cache_size_bytes': total_size,
            'total_cache_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_directory': str(self.cache_dir)
        }
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired cache entries
        
        Returns:
            Number of expired entries removed
        """
        count = 0
        
        for cache_subdir in [self.video_cache_dir, self.comments_cache_dir, self.search_cache_dir]:
            for cache_file in cache_subdir.glob('*.json'):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_at = cache_data.get('cached_at', 0)
                    ttl = cache_data.get('ttl', self.default_ttl)
                    
                    if time.time() - cached_at > ttl:
                        cache_file.unlink()
                        count += 1
                except (json.JSONDecodeError, IOError, OSError, KeyError):
                    # Invalid cache file, remove it
                    cache_file.unlink()
                    count += 1
        
        return count


if __name__ == "__main__":
    # Test the cache manager
    print("Testing Cache Manager...")
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=10)
    
    # Test video caching
    test_data = {'video_id': 'test123', 'title': 'Test Video'}
    cache.set('video', 'test123', test_data)
    
    retrieved = cache.get('video', 'test123')
    assert retrieved == test_data, "Cache retrieval failed"
    print("✓ Cache set and get working")
    
    # Test stats
    stats = cache.get_stats()
    print(f"✓ Cache stats: {stats}")
    
    # Test clear
    count = cache.clear()
    print(f"✓ Cleared {count} cache entries")
    
    # Cleanup test cache directory
    import shutil
    shutil.rmtree('.cache_test')
    
    print("\n✅ All cache manager tests passed!")
