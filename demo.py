#!/usr/bin/env python3
"""
Demo script showing example output format
Runs without requiring API keys
"""

from recommendation_engine import RecommendationEngine
from sentiment_analyzer import SentimentAnalyzer


def print_demo_banner():
    """Print demo banner"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🎥  YouTube SEO Analyzer & Optimizer  🎥            ║
    ║                                                               ║
    ║         AI-Powered Video Analysis & Recommendations          ║
    ║                         DEMO MODE                             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


def demo_analysis():
    """Run a demo analysis with sample data"""
    
    print_demo_banner()
    
    print("🔍 Analyzing video: https://www.youtube.com/watch?v=EXAMPLE123")
    print("-" * 70)
    print("Analyzing video: EXAMPLE123")
    print("✓ Fetched metadata for: Ultimate Python Tutorial 2024 | Complete Guide")
    print("✓ Calculated engagement metrics")
    print("✓ Fetched 87 comments")
    print("✓ Found 5 top-ranking videos in niche")
    
    # Sample video data
    print("\n" + "="*70)
    print("📹 VIDEO INFORMATION")
    print("="*70)
    print("Title: Ultimate Python Tutorial 2024 | Complete Guide for Beginners")
    print("Channel: TechMaster Academy")
    print("Published: 2024-01-15")
    print("Duration: PT15M30S")
    print("Video ID: EXAMPLE123")
    print("Category: 28 (Science & Technology)")
    
    print("\n" + "="*70)
    print("📊 STATISTICS & METRICS")
    print("="*70)
    print("Views: 15,430")
    print("Likes: 850")
    print("Comments: 127")
    
    print("\nEngagement Rate: 6.33%")
    print("Like Rate: 5.51%")
    print("Comment Rate: 0.82%")
    print("Estimated CTR: 8.5%")
    
    # Sentiment analysis demo
    print("\n🧠 Analyzing comment sentiment...")
    
    sample_comments = [
        "This is the best Python tutorial I've ever seen! Finally someone who explains it clearly.",
        "Very helpful, thank you so much for this content!",
        "Great video! Subscribed immediately.",
        "Good content, but the audio could be better.",
        "Excellent explanation of complex topics. Keep it up!",
        "Not bad, but I've seen better tutorials.",
        "Amazing! This helped me land my first job!",
        "Perfect for beginners like me. Thank you!",
        "The examples are super clear and easy to follow.",
        "Love your teaching style!"
    ]
    
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_data = sentiment_analyzer.analyze_comments(sample_comments)
    
    print("\n" + "="*70)
    print("💭 SENTIMENT ANALYSIS")
    print("="*70)
    print(f"Total Comments Analyzed: {sentiment_data['total_comments']}")
    print(f"\nOverall Sentiment: {sentiment_data['overall_sentiment'].upper()}")
    print(f"Average Polarity: {sentiment_data['average_polarity']}")
    print(f"\nSentiment Distribution:")
    print(f"  Positive: {sentiment_data['sentiment_percentages']['positive']}% ({sentiment_data['sentiment_distribution']['positive']} comments)")
    print(f"  Neutral:  {sentiment_data['sentiment_percentages']['neutral']}% ({sentiment_data['sentiment_distribution']['neutral']} comments)")
    print(f"  Negative: {sentiment_data['sentiment_percentages']['negative']}% ({sentiment_data['sentiment_distribution']['negative']} comments)")
    
    # Top videos comparison
    print("\n" + "="*70)
    print("🏆 TOP VIDEOS IN NICHE (Comparison)")
    print("="*70)
    print("Average Views of Top Videos: 45,230")
    print("Your Video Views: 15,430")
    print("Gap: 65.9% below average")
    
    print("\nTop 5 Videos:")
    print("  1. Python Full Course for Beginners 2024...")
    print("     Views: 125,400 | Likes: 8,230")
    print("  2. Learn Python Programming - Complete Tutorial...")
    print("     Views: 89,650 | Likes: 5,120")
    print("  3. Python Tutorial: Getting Started with Python...")
    print("     Views: 67,890 | Likes: 4,560")
    print("  4. Master Python in 30 Days - Full Course...")
    print("     Views: 45,230 | Likes: 3,100")
    print("  5. Python Programming for Beginners - Step by Step...")
    print("     Views: 38,980 | Likes: 2,890")
    
    # Generate and display recommendations
    print("\n🤖 Generating SEO recommendations...")
    
    analysis_data = {
        'metadata': {
            'video_id': 'EXAMPLE123',
            'title': 'Ultimate Python Tutorial 2024 | Complete Guide for Beginners',
            'description': 'In this comprehensive Python tutorial, learn everything you need to know to start programming in Python. Perfect for complete beginners! We cover variables, functions, loops, and more. Follow along with practical examples.',
            'tags': ['python', 'programming', 'tutorial', 'beginners', 'coding'],
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'statistics': {
                'view_count': 15430,
                'like_count': 850,
                'comment_count': 127,
                'favorite_count': 0
            },
            'channel_statistics': {
                'subscriber_count': 50000,
                'video_count': 150,
                'view_count': 2000000
            }
        },
        'engagement': {
            'engagement_rate': 6.33,
            'like_rate': 5.51,
            'comment_rate': 0.82,
            'estimated_ctr': 8.5
        },
        'top_videos': [
            {'video_id': 'top1', 'title': 'Python Full Course', 'view_count': 125400, 'tags': ['python', 'full course', 'tutorial', 'beginners', '2024']}
        ],
        'sentiment': sentiment_data
    }
    
    rec_engine = RecommendationEngine(api_key=None)
    recommendations = rec_engine.generate_recommendations(analysis_data)
    report = rec_engine.generate_report(recommendations)
    
    print("\n" + report)
    
    print("\n✅ Analysis complete!")
    print("\nNext Steps:")
    print("  1. Review the recommendations above")
    print("  2. Implement suggested optimizations")
    print("  3. Monitor performance after changes")
    print("  4. Re-analyze after 1-2 weeks to track improvement")
    
    print("\n" + "="*70)
    print("💡 TIP: This is a demo with sample data.")
    print("To analyze real videos:")
    print("  1. Set up API keys in .env file")
    print("  2. Run: python youseo.py https://www.youtube.com/watch?v=VIDEO_ID")
    print("="*70)


if __name__ == "__main__":
    demo_analysis()
