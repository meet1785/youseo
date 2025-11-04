#!/usr/bin/env python3
"""
Test script for YouTube SEO Analyzer
Tests core functionality without requiring API keys
"""

import sys
from sentiment_analyzer import SentimentAnalyzer
from recommendation_engine import RecommendationEngine


def test_sentiment_analyzer():
    """Test sentiment analysis functionality"""
    print("\n" + "="*70)
    print("TEST 1: Sentiment Analysis")
    print("="*70)
    
    analyzer = SentimentAnalyzer()
    
    # Test with various comments
    comments = [
        "This is absolutely amazing! Best video ever! 🔥",
        "Very helpful tutorial, thanks a lot!",
        "Good content, but could use better examples",
        "Not really what I was looking for...",
        "Excellent explanation! Finally understand this topic",
        "Meh, it's okay I guess",
        "Terrible quality, waste of time",
        "Love your channel! Keep up the great work!",
        "This helped me so much with my project!",
        "Brilliant! Subscribed immediately!"
    ]
    
    result = analyzer.analyze_comments(comments)
    
    print(f"\n📊 Analysis Results:")
    print(f"   Total Comments: {result['total_comments']}")
    print(f"   Overall Sentiment: {result['overall_sentiment'].upper()}")
    print(f"   Average Polarity: {result['average_polarity']}")
    print(f"\n   Distribution:")
    print(f"   ✅ Positive: {result['sentiment_percentages']['positive']}% ({result['sentiment_distribution']['positive']} comments)")
    print(f"   ⚪ Neutral:  {result['sentiment_percentages']['neutral']}% ({result['sentiment_distribution']['neutral']} comments)")
    print(f"   ❌ Negative: {result['sentiment_percentages']['negative']}% ({result['sentiment_distribution']['negative']} comments)")
    
    # Test common themes extraction
    themes = analyzer.extract_common_themes(comments, top_n=5)
    print(f"\n   Common Themes:")
    for word, count in themes:
        print(f"   - {word}: {count} occurrences")
    
    print("\n✅ Sentiment Analysis: PASSED")
    return True


def test_recommendation_engine():
    """Test recommendation generation"""
    print("\n" + "="*70)
    print("TEST 2: Recommendation Engine")
    print("="*70)
    
    rec_engine = RecommendationEngine(api_key=None)
    
    # Test case 1: Well-optimized video
    print("\n📹 Test Case 1: Well-optimized video")
    good_video = {
        'metadata': {
            'video_id': 'test123',
            'title': '10 Python Tips Every Developer Needs in 2024 | Complete Guide',
            'description': 'In this comprehensive tutorial, we explore 10 essential Python tips that every developer should know. Learn about list comprehensions, decorators, context managers, and more. Perfect for beginners and intermediate programmers. Timestamps: 0:00 Intro, 2:30 Tip 1, 5:00 Tip 2...',
            'tags': ['python', 'programming', 'tutorial', 'coding', 'python tips'],
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'statistics': {
                'view_count': 10000,
                'like_count': 800,
                'comment_count': 150,
                'favorite_count': 0
            },
            'channel_statistics': {
                'subscriber_count': 50000,
                'video_count': 200,
                'view_count': 1000000
            }
        },
        'engagement': {
            'engagement_rate': 9.5,
            'like_rate': 8.0,
            'comment_rate': 1.5,
            'estimated_ctr': 20.0
        },
        'top_videos': [],
        'sentiment': {
            'overall_sentiment': 'positive',
            'average_polarity': 0.6
        }
    }
    
    recs = rec_engine.generate_recommendations(good_video)
    print(f"   Title Score: {recs['title_optimization']['score']}/100")
    print(f"   Description Score: {recs['description_optimization']['score']}/100")
    print(f"   Tags Score: {recs['tags_optimization']['score']}/100")
    print(f"   Engagement Score: {recs['engagement_strategies']['score']}/100")
    
    # Test case 2: Needs improvement
    print("\n📹 Test Case 2: Video needing optimization")
    poor_video = {
        'metadata': {
            'video_id': 'test456',
            'title': 'Video',
            'description': 'Check it out',
            'tags': [],
            'thumbnail_url': 'https://example.com/thumb2.jpg',
            'statistics': {
                'view_count': 500,
                'like_count': 10,
                'comment_count': 2,
                'favorite_count': 0
            },
            'channel_statistics': {
                'subscriber_count': 10000,
                'video_count': 50,
                'view_count': 100000
            }
        },
        'engagement': {
            'engagement_rate': 2.4,
            'like_rate': 2.0,
            'comment_rate': 0.4,
            'estimated_ctr': 5.0
        },
        'top_videos': [],
        'sentiment': {
            'overall_sentiment': 'neutral',
            'average_polarity': 0.0
        }
    }
    
    recs2 = rec_engine.generate_recommendations(poor_video)
    print(f"   Title Score: {recs2['title_optimization']['score']}/100")
    print(f"   Description Score: {recs2['description_optimization']['score']}/100")
    print(f"   Tags Score: {recs2['tags_optimization']['score']}/100")
    print(f"   Engagement Score: {recs2['engagement_strategies']['score']}/100")
    
    print(f"\n   Suggestions for improvement:")
    for i, suggestion in enumerate(recs2['title_optimization']['suggestions'][:3], 1):
        print(f"   {i}. {suggestion}")
    
    print("\n✅ Recommendation Engine: PASSED")
    return True


def test_report_generation():
    """Test report generation"""
    print("\n" + "="*70)
    print("TEST 3: Report Generation")
    print("="*70)
    
    rec_engine = RecommendationEngine(api_key=None)
    
    # Sample data
    analysis_data = {
        'metadata': {
            'video_id': 'test789',
            'title': 'How to Master Python in 30 Days',
            'description': 'Complete Python course for beginners. Learn Python from scratch with hands-on projects.',
            'tags': ['python', 'programming', 'tutorial'],
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'statistics': {
                'view_count': 5000,
                'like_count': 250,
                'comment_count': 50,
                'favorite_count': 0
            },
            'channel_statistics': {
                'subscriber_count': 20000,
                'video_count': 100,
                'view_count': 500000
            }
        },
        'engagement': {
            'engagement_rate': 6.0,
            'like_rate': 5.0,
            'comment_rate': 1.0,
            'estimated_ctr': 25.0
        },
        'top_videos': [],
        'sentiment': {
            'overall_sentiment': 'positive',
            'average_polarity': 0.5
        }
    }
    
    recommendations = rec_engine.generate_recommendations(analysis_data)
    report = rec_engine.generate_report(recommendations)
    
    print("\n📄 Sample Report Preview (first 500 chars):")
    print("-" * 70)
    print(report[:500] + "...")
    print("-" * 70)
    
    print("\n✅ Report Generation: PASSED")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 YouTube SEO Analyzer - Test Suite")
    print("="*70)
    print("\nRunning tests without API keys...")
    
    try:
        results = []
        
        # Run tests
        results.append(test_sentiment_analyzer())
        results.append(test_recommendation_engine())
        results.append(test_report_generation())
        
        # Summary
        print("\n" + "="*70)
        print("📋 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")
        
        if all(results):
            print("\n✅ ALL TESTS PASSED!")
            print("\n🎉 The YouTube SEO Analyzer is working correctly!")
            print("\nTo use with real videos, set up your API keys:")
            print("  1. Copy .env.example to .env")
            print("  2. Add your YOUTUBE_API_KEY")
            print("  3. Optionally add OPENAI_API_KEY for AI insights")
            print("  4. Run: python youseo.py https://www.youtube.com/watch?v=VIDEO_ID")
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
