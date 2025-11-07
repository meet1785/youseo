#!/usr/bin/env python3
"""
Test script for cache manager functionality
Tests cache operations and integration with YouTube analyzer
"""

import sys
import os
import time
import shutil
from cache_manager import CacheManager


def test_cache_manager_basic():
    """Test basic cache manager operations"""
    print("\n" + "="*70)
    print("TEST 1: Basic Cache Manager Operations")
    print("="*70)
    
    # Create test cache
    cache = CacheManager(cache_dir='.cache_test', default_ttl=10)
    
    # Test video caching
    test_video = {
        'video_id': 'test123',
        'title': 'Test Video',
        'views': 1000
    }
    
    # Set cache
    success = cache.set('video', 'test123', test_video)
    assert success, "Failed to set cache"
    print("✓ Cache set successfully")
    
    # Get cache
    retrieved = cache.get('video', 'test123')
    assert retrieved == test_video, "Retrieved data doesn't match"
    print("✓ Cache retrieval successful")
    
    # Test cache miss
    missing = cache.get('video', 'nonexistent')
    assert missing is None, "Should return None for missing cache"
    print("✓ Cache miss handled correctly")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Basic Cache Manager: PASSED")
    return True


def test_cache_ttl():
    """Test cache TTL (Time-To-Live) functionality"""
    print("\n" + "="*70)
    print("TEST 2: Cache TTL (Time-To-Live)")
    print("="*70)
    
    # Create cache with 2 second TTL
    cache = CacheManager(cache_dir='.cache_test', default_ttl=2)
    
    test_data = {'test': 'data'}
    cache.set('video', 'ttl_test', test_data)
    
    # Should be available immediately
    retrieved = cache.get('video', 'ttl_test')
    assert retrieved == test_data, "Cache should be available immediately"
    print("✓ Cache available immediately after set")
    
    # Wait for TTL to expire
    print("  Waiting 3 seconds for TTL to expire...")
    time.sleep(3)
    
    # Should be expired
    expired = cache.get('video', 'ttl_test')
    assert expired is None, "Cache should be expired"
    print("✓ Cache expired after TTL")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cache TTL: PASSED")
    return True


def test_cache_types():
    """Test different cache types (video, comments, search)"""
    print("\n" + "="*70)
    print("TEST 3: Cache Types")
    print("="*70)
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=60)
    
    # Test video cache
    video_data = {'video_id': 'v1', 'title': 'Video 1'}
    cache.set('video', 'v1', video_data)
    assert cache.get('video', 'v1') == video_data
    print("✓ Video cache working")
    
    # Test comments cache
    comments_data = ['comment1', 'comment2']
    cache.set('comments', 'v1_100', comments_data)
    assert cache.get('comments', 'v1_100') == comments_data
    print("✓ Comments cache working")
    
    # Test search cache
    search_data = [{'video_id': 's1'}, {'video_id': 's2'}]
    cache.set('search', 'query1_5', search_data)
    assert cache.get('search', 'query1_5') == search_data
    print("✓ Search cache working")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cache Types: PASSED")
    return True


def test_cache_stats():
    """Test cache statistics"""
    print("\n" + "="*70)
    print("TEST 4: Cache Statistics")
    print("="*70)
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=60)
    
    # Add some data
    cache.set('video', 'v1', {'data': 'test1'})
    cache.set('video', 'v2', {'data': 'test2'})
    cache.set('comments', 'c1', ['comment1'])
    cache.set('search', 's1', [{'result': 1}])
    
    # Get stats
    stats = cache.get_stats()
    
    assert stats['video']['total'] == 2, "Should have 2 video cache entries"
    assert stats['comments']['total'] == 1, "Should have 1 comments cache entry"
    assert stats['search']['total'] == 1, "Should have 1 search cache entry"
    assert stats['total_cache_size_bytes'] > 0, "Cache size should be > 0"
    
    print(f"✓ Cache stats: {stats['video']['total']} videos, "
          f"{stats['comments']['total']} comments, "
          f"{stats['search']['total']} searches")
    print(f"✓ Total cache size: {stats['total_cache_size_mb']} MB")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cache Statistics: PASSED")
    return True


def test_cache_clear():
    """Test cache clearing functionality"""
    print("\n" + "="*70)
    print("TEST 5: Cache Clear")
    print("="*70)
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=60)
    
    # Add data
    cache.set('video', 'v1', {'data': 'test'})
    cache.set('comments', 'c1', ['comment'])
    cache.set('search', 's1', [{'result': 1}])
    
    # Clear video cache only
    count = cache.clear('video')
    assert count == 1, "Should clear 1 video cache entry"
    print(f"✓ Cleared {count} video cache entries")
    
    # Verify video cache cleared but others remain
    assert cache.get('video', 'v1') is None
    assert cache.get('comments', 'c1') is not None
    assert cache.get('search', 's1') is not None
    print("✓ Selective cache clear working")
    
    # Clear all
    count = cache.clear()
    assert count == 2, "Should clear remaining 2 entries"
    print(f"✓ Cleared all {count} remaining entries")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cache Clear: PASSED")
    return True


def test_cache_invalidate():
    """Test cache invalidation"""
    print("\n" + "="*70)
    print("TEST 6: Cache Invalidation")
    print("="*70)
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=60)
    
    # Add data
    cache.set('video', 'v1', {'data': 'test'})
    assert cache.get('video', 'v1') is not None
    
    # Invalidate specific entry
    success = cache.invalidate('video', 'v1')
    assert success, "Should successfully invalidate"
    print("✓ Cache entry invalidated")
    
    # Verify it's gone
    assert cache.get('video', 'v1') is None
    print("✓ Invalidated entry no longer available")
    
    # Try invalidating non-existent entry
    success = cache.invalidate('video', 'nonexistent')
    assert not success, "Should return False for non-existent entry"
    print("✓ Invalidating non-existent entry handled correctly")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cache Invalidation: PASSED")
    return True


def test_cache_cleanup_expired():
    """Test cleanup of expired cache entries"""
    print("\n" + "="*70)
    print("TEST 7: Cleanup Expired Entries")
    print("="*70)
    
    cache = CacheManager(cache_dir='.cache_test', default_ttl=2)
    
    # Add data with short TTL
    cache.set('video', 'v1', {'data': 'test1'})
    cache.set('video', 'v2', {'data': 'test2'})
    
    # Wait for expiration
    print("  Waiting 3 seconds for cache to expire...")
    time.sleep(3)
    
    # Add new data (should not expire)
    cache.set('video', 'v3', {'data': 'test3'})
    
    # Cleanup expired
    count = cache.cleanup_expired()
    assert count == 2, "Should clean up 2 expired entries"
    print(f"✓ Cleaned up {count} expired entries")
    
    # Verify new data still exists
    assert cache.get('video', 'v3') is not None
    print("✓ Non-expired entries preserved")
    
    # Cleanup
    shutil.rmtree('.cache_test')
    print("\n✅ Cleanup Expired: PASSED")
    return True


def main():
    """Run all cache tests"""
    print("\n" + "="*70)
    print("🧪 Cache Manager - Test Suite")
    print("="*70)
    print("\nRunning comprehensive cache tests...")
    
    try:
        results = []
        
        # Run all tests
        results.append(test_cache_manager_basic())
        results.append(test_cache_ttl())
        results.append(test_cache_types())
        results.append(test_cache_stats())
        results.append(test_cache_clear())
        results.append(test_cache_invalidate())
        results.append(test_cache_cleanup_expired())
        
        # Summary
        print("\n" + "="*70)
        print("📋 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")
        
        if all(results):
            print("\n✅ ALL CACHE TESTS PASSED!")
            print("\n🎉 Cache functionality is working correctly!")
            print("\nCache features available:")
            print("  • Automatic caching of API responses")
            print("  • Configurable TTL for different cache types")
            print("  • Cache statistics and monitoring")
            print("  • Manual cache management (clear, invalidate)")
            print("  • Automatic cleanup of expired entries")
            return 0
        else:
            print("\n❌ SOME TESTS FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
