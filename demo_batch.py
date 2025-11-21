#!/usr/bin/env python3
"""
Demo script for Batch Analysis feature
Shows example batch analysis without requiring API keys
"""

import sys
from batch_analyzer import BatchAnalyzer


def create_mock_analyzers():
    """Create mock analyzers with varied performance data"""
    class MockYouTubeAnalyzer:
        def __init__(self):
            self.video_data = {
                'VIDEO1': {
                    'title': 'Complete Python Tutorial 2024 - Beginner to Advanced',
                    'views': 125430,
                    'likes': 5240,
                    'comments': 432
                },
                'VIDEO2': {
                    'title': 'Quick Tip: Speed Up Your Code',
                    'views': 8750,
                    'likes': 420,
                    'comments': 35
                },
                'VIDEO3': {
                    'title': 'Top 10 Python Libraries You Must Know',
                    'views': 45200,
                    'likes': 2100,
                    'comments': 178
                },
                'SHORT1': {
                    'title': '30 Second Python Trick 🔥',
                    'views': 89600,
                    'likes': 8200,
                    'comments': 425
                }
            }
        
        def extract_video_id(self, url):
            if 'watch?v=' in url:
                return url.split('watch?v=')[-1].split('&')[0]
            elif 'shorts/' in url:
                return url.split('shorts/')[-1].split('?')[0]
            return None
        
        def analyze_video(self, url):
            video_id = self.extract_video_id(url)
            data = self.video_data.get(video_id, self.video_data['VIDEO1'])
            
            return {
                'metadata': {
                    'video_id': video_id,
                    'title': data['title'],
                    'channel_title': 'TechTutorials Pro',
                    'statistics': {
                        'view_count': data['views'],
                        'like_count': data['likes'],
                        'comment_count': data['comments']
                    }
                },
                'engagement': {
                    'engagement_rate': round((data['likes'] + data['comments']) / data['views'] * 100, 2),
                    'like_rate': round(data['likes'] / data['views'] * 100, 2),
                    'comment_rate': round(data['comments'] / data['views'] * 100, 2)
                },
                'comments': [
                    'Great tutorial! Very helpful 👍',
                    'This helped me understand the concept',
                    'Amazing explanation!',
                    'Could you make more videos like this?',
                    'Thanks for sharing this!'
                ]
            }
    
    class MockSentimentAnalyzer:
        def analyze_comments(self, comments):
            return {
                'total_comments': len(comments),
                'overall_sentiment': 'positive',
                'average_polarity': 0.65
            }
    
    class MockRecommendationEngine:
        def generate_recommendations(self, analysis_data):
            return {
                'title_optimization': {
                    'score': 85,
                    'suggestions': ['Title is well-optimized']
                },
                'description_optimization': {
                    'score': 75,
                    'suggestions': ['Add more keywords in description']
                },
                'tags_optimization': {
                    'score': 80,
                    'suggestions': ['Consider adding 2-3 more relevant tags']
                }
            }
    
    return MockYouTubeAnalyzer(), MockSentimentAnalyzer(), MockRecommendationEngine()


def print_demo_banner():
    """Print demo banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🎥  YouTube SEO Analyzer - Batch Analysis Demo  🎥        ║
║                                                                   ║
║              Demonstrating Multi-Video Analysis                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)


def main():
    """Run batch analysis demo"""
    print_demo_banner()
    
    print("This demo shows how batch analysis works without requiring API keys.")
    print("In real usage, the tool analyzes actual YouTube videos via the API.\n")
    
    # Create mock analyzers
    youtube_analyzer, sentiment_analyzer, recommendation_engine = create_mock_analyzers()
    
    # Create batch analyzer
    batch = BatchAnalyzer(youtube_analyzer, sentiment_analyzer, recommendation_engine)
    
    # Sample URLs
    urls = [
        "https://www.youtube.com/watch?v=VIDEO1",
        "https://www.youtube.com/watch?v=VIDEO2",
        "https://www.youtube.com/watch?v=VIDEO3",
        "https://www.youtube.com/shorts/SHORT1"
    ]
    
    print("📋 Demo: Analyzing 4 videos from a hypothetical Python tutorial channel\n")
    
    # Analyze videos
    results = batch.analyze_videos(urls, analyze_comments=True)
    
    # Print summary report
    batch.print_summary_report()
    
    # Show export capability
    print("\n" + "="*70)
    print("📦 EXPORT CAPABILITIES")
    print("="*70)
    print("\nBatch results can be exported in two formats:")
    print("\n1. JSON Format (detailed):")
    print("   - Complete analysis data for each video")
    print("   - All recommendations and metrics")
    print("   - Summary statistics")
    print("   - Best for programmatic processing")
    
    print("\n2. CSV Format (spreadsheet-friendly):")
    print("   - Key metrics in tabular format")
    print("   - Easy to import into Excel/Sheets")
    print("   - Perfect for quick comparisons")
    print("   - Great for creating charts")
    
    print("\n" + "="*70)
    print("💡 KEY INSIGHTS FROM DEMO")
    print("="*70)
    print("\nFrom this batch analysis, we learned:")
    print("  1. The 'Complete Tutorial' video has highest views (125K)")
    print("  2. The 'Quick Tip' video needs improvement (only 8.7K views)")
    print("  3. The Short has highest engagement rate (9.6%)")
    print("  4. Overall positive sentiment across all videos")
    print("\n📊 Action items:")
    print("  • Apply title/thumbnail strategies from top performer to low performers")
    print("  • Consider creating more Shorts (high engagement)")
    print("  • Maintain positive community engagement")
    
    print("\n" + "="*70)
    print("🚀 REAL USAGE")
    print("="*70)
    print("\nTo use batch analysis with real videos:")
    print("\n1. Create a file with your video URLs (videos.txt):")
    print("   https://www.youtube.com/watch?v=YOUR_VIDEO_1")
    print("   https://www.youtube.com/watch?v=YOUR_VIDEO_2")
    print("   https://www.youtube.com/shorts/YOUR_SHORT_1")
    
    print("\n2. Set up your YouTube API key in .env file")
    
    print("\n3. Run batch analysis:")
    print("   python youseo.py --batch videos.txt")
    
    print("\n4. Export results:")
    print("   python youseo.py --batch videos.txt --batch-output results.json")
    print("   python youseo.py --batch videos.txt --batch-format csv")
    
    print("\n" + "="*70)
    print("\n✅ Demo complete! The batch analysis feature allows you to:")
    print("   • Analyze multiple videos in one command")
    print("   • Compare performance across your content")
    print("   • Identify patterns and opportunities")
    print("   • Export data for further analysis")
    print("\n🎉 Happy analyzing!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
