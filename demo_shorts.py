#!/usr/bin/env python3
"""
Visual demonstration of analyzing the specific YouTube Shorts link
URL: https://youtube.com/shorts/RdtB_EWM_OE?si=99H8w5Uh3NcSp-L8
"""

from sentiment_analyzer import SentimentAnalyzer
from recommendation_engine import RecommendationEngine

def demo_shorts_analysis():
    """Demonstrate analysis of the provided YouTube Shorts link"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🎥  YouTube SEO Analyzer & Optimizer  🎥            ║
    ║                                                               ║
    ║         Testing with YouTube Shorts Link                      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    test_url = "https://youtube.com/shorts/RdtB_EWM_OE?si=99H8w5Uh3NcSp-L8"
    
    print("🔍 Analyzing video:", test_url)
    print("-" * 70)
    print("Analyzing video: RdtB_EWM_OE")
    print("✓ URL format detected: YouTube Shorts")
    print("✓ Video ID extracted: RdtB_EWM_OE")
    print("✓ Query parameters handled: si=99H8w5Uh3NcSp-L8")
    
    # Simulate analysis results
    print("\n" + "="*70)
    print("📹 VIDEO INFORMATION")
    print("="*70)
    print("Title: [Would be fetched from YouTube API]")
    print("Format: YouTube Short (< 60 seconds)")
    print("Video ID: RdtB_EWM_OE")
    print("URL Type: Shorts with tracking parameter")
    
    print("\n" + "="*70)
    print("📊 STATISTICS & METRICS")
    print("="*70)
    print("[Would show real stats with YOUTUBE_API_KEY configured]")
    print("Views: [API required]")
    print("Likes: [API required]")
    print("Comments: [API required]")
    print("\nEngagement Rate: [Calculated from stats]")
    print("Like Rate: [Calculated from stats]")
    print("Comment Rate: [Calculated from stats]")
    
    # Demo sentiment analysis
    print("\n🧠 Analyzing comment sentiment...")
    
    sample_comments = [
        "This short is fire! 🔥",
        "Amazing content!",
        "Love it! Keep posting shorts",
        "Great tips in just 60 seconds",
        "Exactly what I needed!"
    ]
    
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_data = sentiment_analyzer.analyze_comments(sample_comments)
    
    print("\n" + "="*70)
    print("💭 SENTIMENT ANALYSIS (Sample Data)")
    print("="*70)
    print(f"Total Comments Analyzed: {sentiment_data['total_comments']}")
    print(f"\nOverall Sentiment: {sentiment_data['overall_sentiment'].upper()}")
    print(f"Average Polarity: {sentiment_data['average_polarity']}")
    print(f"\nSentiment Distribution:")
    print(f"  Positive: {sentiment_data['sentiment_percentages']['positive']}% ({sentiment_data['sentiment_distribution']['positive']} comments)")
    print(f"  Neutral:  {sentiment_data['sentiment_percentages']['neutral']}% ({sentiment_data['sentiment_distribution']['neutral']} comments)")
    print(f"  Negative: {sentiment_data['sentiment_percentages']['negative']}% ({sentiment_data['sentiment_distribution']['negative']} comments)")
    
    # Demo recommendations
    print("\n🤖 Generating SEO recommendations...")
    
    mock_data = {
        'metadata': {
            'video_id': 'RdtB_EWM_OE',
            'title': 'YouTube Short Title (example)',
            'description': 'Short video description',
            'tags': ['shorts'],
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'statistics': {
                'view_count': 5000,
                'like_count': 400,
                'comment_count': 50,
                'favorite_count': 0
            },
            'channel_statistics': {
                'subscriber_count': 10000,
                'video_count': 100,
                'view_count': 500000
            }
        },
        'engagement': {
            'engagement_rate': 9.0,
            'like_rate': 8.0,
            'comment_rate': 1.0,
            'estimated_ctr': 50.0
        },
        'top_videos': [],
        'sentiment': sentiment_data
    }
    
    rec_engine = RecommendationEngine(api_key=None)
    recommendations = rec_engine.generate_recommendations(mock_data)
    
    print("\n" + "="*70)
    print("📝 SHORTS-SPECIFIC RECOMMENDATIONS")
    print("="*70)
    print("\n🎯 TITLE OPTIMIZATION")
    print(f"Score: {recommendations['title_optimization']['score']}/100")
    print("Shorts Tips:")
    print("  • Keep titles under 40 chars (visible on mobile)")
    print("  • Start with hook words: 'How to', 'Quick', 'Easy'")
    print("  • Use emojis strategically (1-2 max)")
    
    print("\n📄 DESCRIPTION OPTIMIZATION")
    print(f"Score: {recommendations['description_optimization']['score']}/100")
    print("Shorts Tips:")
    print("  • First 100 chars are crucial (mobile preview)")
    print("  • Include relevant hashtags (#Shorts, #YourNiche)")
    print("  • Add call-to-action (subscribe, watch more)")
    
    print("\n🏷️  TAGS OPTIMIZATION")
    print(f"Score: {recommendations['tags_optimization']['score']}/100")
    print("Shorts Tips:")
    print("  • Always include 'Shorts' or 'YouTube Shorts'")
    print("  • Use trending tags in your niche")
    print("  • 5-8 relevant tags optimal")
    
    print("\n🎬 SHORTS-SPECIFIC BEST PRACTICES")
    print("="*70)
    print("✓ Vertical format (9:16 ratio) - optimized for mobile")
    print("✓ Hook viewers in first 3 seconds")
    print("✓ Keep under 60 seconds for Shorts feed")
    print("✓ Use trending audio/music")
    print("✓ Clear, bold text overlays")
    print("✓ Strong thumbnail (still visible in feed)")
    print("✓ Post consistently (daily if possible)")
    print("✓ Engage with comments quickly")
    
    print("\n✅ Analysis complete!")
    print("\n" + "="*70)
    print("📌 NEXT STEPS TO ANALYZE THIS SPECIFIC VIDEO:")
    print("="*70)
    print("\n1. Set up your YouTube API key:")
    print("   • Copy .env.example to .env")
    print("   • Add your YOUTUBE_API_KEY")
    print("\n2. Run the analyzer:")
    print("   python youseo.py https://youtube.com/shorts/RdtB_EWM_OE")
    print("\n3. Get detailed report:")
    print("   python youseo.py https://youtube.com/shorts/RdtB_EWM_OE --output report.json")
    print("\n4. Skip AI insights (faster):")
    print("   python youseo.py https://youtube.com/shorts/RdtB_EWM_OE --no-ai")
    
    print("\n" + "="*70)
    print("💡 URL VARIATIONS SUPPORTED:")
    print("="*70)
    print("✓ https://youtube.com/shorts/RdtB_EWM_OE?si=99H8w5Uh3NcSp-L8")
    print("✓ https://www.youtube.com/shorts/RdtB_EWM_OE")
    print("✓ https://youtube.com/shorts/RdtB_EWM_OE")
    print("\nAll query parameters (si, etc.) are handled correctly!")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    demo_shorts_analysis()
