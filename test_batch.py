#!/usr/bin/env python3
"""
Test script for Batch Analysis functionality
Tests batch processing without requiring API keys
"""

import sys
import os
import tempfile
from pathlib import Path
from batch_analyzer import BatchAnalyzer


def create_mock_analyzer():
    """Create a mock analyzer for testing"""
    class MockYouTubeAnalyzer:
        def extract_video_id(self, url):
            """Extract mock video ID"""
            if 'watch?v=' in url:
                return url.split('watch?v=')[-1].split('&')[0]
            elif 'shorts/' in url:
                return url.split('shorts/')[-1].split('?')[0]
            return None
        
        def analyze_video(self, url):
            """Return mock analysis data"""
            video_id = self.extract_video_id(url)
            return {
                'metadata': {
                    'video_id': video_id,
                    'title': f'Test Video {video_id}',
                    'channel_title': 'Test Channel',
                    'statistics': {
                        'view_count': 10000,
                        'like_count': 500,
                        'comment_count': 50
                    }
                },
                'engagement': {
                    'engagement_rate': 5.5,
                    'like_rate': 5.0,
                    'comment_rate': 0.5
                },
                'comments': ['Great video!', 'Very helpful', 'Thanks!']
            }
    
    class MockSentimentAnalyzer:
        def analyze_comments(self, comments):
            """Return mock sentiment data"""
            return {
                'total_comments': len(comments),
                'overall_sentiment': 'positive',
                'average_polarity': 0.5
            }
    
    class MockRecommendationEngine:
        def generate_recommendations(self, analysis_data):
            """Return mock recommendations"""
            return {
                'title_optimization': {'score': 80, 'suggestions': []},
                'description_optimization': {'score': 75, 'suggestions': []},
                'tags_optimization': {'score': 70, 'suggestions': []}
            }
    
    return MockYouTubeAnalyzer(), MockSentimentAnalyzer(), MockRecommendationEngine()


def test_parse_txt_file():
    """Test parsing URLs from a .txt file"""
    print("\n" + "="*70)
    print("TEST 1: Parse URLs from TXT file")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# Test URLs\n")
        f.write("https://www.youtube.com/watch?v=VIDEO1\n")
        f.write("https://www.youtube.com/watch?v=VIDEO2\n")
        f.write("\n")  # Empty line
        f.write("https://www.youtube.com/shorts/VIDEO3\n")
        temp_file = f.name
    
    try:
        urls = batch.parse_urls_from_file(temp_file)
        print(f"✓ Parsed {len(urls)} URLs from TXT file")
        assert len(urls) == 3, "Should parse 3 URLs"
        assert urls[0] == "https://www.youtube.com/watch?v=VIDEO1"
        assert urls[2] == "https://www.youtube.com/shorts/VIDEO3"
        print("✓ URLs correctly extracted")
        print("\n✅ TXT File Parsing: PASSED")
        return True
    finally:
        os.unlink(temp_file)


def test_parse_csv_file():
    """Test parsing URLs from a .csv file"""
    print("\n" + "="*70)
    print("TEST 2: Parse URLs from CSV file")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    # Create temporary test file with header
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("URL,Title,Views\n")
        f.write("https://www.youtube.com/watch?v=CSV1,Test 1,1000\n")
        f.write("https://www.youtube.com/watch?v=CSV2,Test 2,2000\n")
        temp_file = f.name
    
    try:
        urls = batch.parse_urls_from_file(temp_file)
        print(f"✓ Parsed {len(urls)} URLs from CSV file")
        assert len(urls) == 2, "Should parse 2 URLs"
        assert urls[0] == "https://www.youtube.com/watch?v=CSV1"
        print("✓ URLs correctly extracted (header skipped)")
        print("\n✅ CSV File Parsing: PASSED")
        return True
    finally:
        os.unlink(temp_file)


def test_batch_analysis():
    """Test batch analysis of multiple videos"""
    print("\n" + "="*70)
    print("TEST 3: Batch Analysis")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    urls = [
        "https://www.youtube.com/watch?v=TEST1",
        "https://www.youtube.com/watch?v=TEST2",
        "https://www.youtube.com/shorts/SHORT1"
    ]
    
    results = batch.analyze_videos(urls, analyze_comments=True)
    
    print(f"\n✓ Analyzed {len(results)} videos")
    assert len(results) == 3, "Should analyze all 3 videos"
    assert 'video_id' in results[0]
    assert 'analysis_data' in results[0]
    assert 'recommendations' in results[0]
    print("✓ Results contain required fields")
    print("\n✅ Batch Analysis: PASSED")
    return True


def test_summary_generation():
    """Test summary statistics generation"""
    print("\n" + "="*70)
    print("TEST 4: Summary Generation")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    urls = [
        "https://www.youtube.com/watch?v=SUMMARY1",
        "https://www.youtube.com/watch?v=SUMMARY2"
    ]
    
    batch.analyze_videos(urls, analyze_comments=False)
    summary = batch.generate_summary()
    
    print("\n📊 Summary Statistics:")
    print(f"  Total Videos: {summary['total_videos']}")
    print(f"  Total Views: {summary['total_views']:,}")
    print(f"  Average Views: {summary['average_views']:,.0f}")
    print(f"  Average Engagement: {summary['average_engagement_rate']:.2f}%")
    
    assert summary['total_videos'] == 2
    assert summary['total_views'] == 20000  # 2 videos * 10000 views each
    assert 'best_performing' in summary
    assert 'worst_performing' in summary
    print("\n✓ Summary contains all expected fields")
    print("\n✅ Summary Generation: PASSED")
    return True


def test_export_json():
    """Test JSON export functionality"""
    print("\n" + "="*70)
    print("TEST 5: JSON Export")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    urls = ["https://www.youtube.com/watch?v=EXPORT1"]
    batch.analyze_videos(urls, analyze_comments=False)
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        batch.export_results(temp_file, format='json')
        
        # Verify file exists and contains data
        import json
        with open(temp_file, 'r') as f:
            data = json.load(f)
        
        assert 'summary' in data
        assert 'videos' in data
        assert len(data['videos']) == 1
        print("\n✓ JSON file created successfully")
        print("✓ JSON contains summary and video data")
        print("\n✅ JSON Export: PASSED")
        return True
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_export_csv():
    """Test CSV export functionality"""
    print("\n" + "="*70)
    print("TEST 6: CSV Export")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    urls = [
        "https://www.youtube.com/watch?v=CSVEXP1",
        "https://www.youtube.com/watch?v=CSVEXP2"
    ]
    batch.analyze_videos(urls, analyze_comments=False)
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_file = f.name
    
    try:
        batch.export_results(temp_file, format='csv')
        
        # Verify file exists and contains data
        with open(temp_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) >= 2  # Header + at least 1 data row
        assert 'title' in lines[0].lower()
        assert 'url' in lines[0].lower()
        assert 'views' in lines[0].lower()
        print("\n✓ CSV file created successfully")
        print(f"✓ CSV contains header and {len(lines) - 1} data rows")
        print("\n✅ CSV Export: PASSED")
        return True
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_invalid_url_handling():
    """Test handling of invalid URLs"""
    print("\n" + "="*70)
    print("TEST 7: Invalid URL Handling")
    print("="*70)
    
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzer()
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    urls = [
        "https://www.youtube.com/watch?v=VALID1",
        "https://not-a-valid-url.com",
        "https://www.youtube.com/watch?v=VALID2"
    ]
    
    results = batch.analyze_videos(urls, analyze_comments=False)
    
    print(f"\n✓ Processed {len(urls)} URLs")
    print(f"✓ Successfully analyzed {len(results)} valid videos")
    assert len(results) == 2, "Should skip invalid URL and continue"
    print("✓ Invalid URLs handled gracefully")
    print("\n✅ Invalid URL Handling: PASSED")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 Batch Analyzer - Test Suite")
    print("="*70)
    print("\nRunning tests without API keys...\n")
    
    tests = [
        test_parse_txt_file,
        test_parse_csv_file,
        test_batch_analysis,
        test_summary_generation,
        test_export_json,
        test_export_csv,
        test_invalid_url_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Print summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        print("\n🎉 Batch analysis functionality is working correctly!")
        print("\nTo use batch analysis:")
        print("  1. Create a file with video URLs (one per line)")
        print("  2. Run: python youseo.py --batch videos.txt")
        print("  3. Or use: python youseo.py --urls URL1 URL2 URL3")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
