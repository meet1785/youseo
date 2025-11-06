#!/usr/bin/env python3
"""
Example usage of YouTube SEO Analyzer
Demonstrates how to use the tool programmatically
"""

from youtube_analyzer import YouTubeSEOAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from recommendation_engine import RecommendationEngine
import json


def example_basic_analysis():
    """Example: Basic video analysis"""
    print("Example 1: Basic Video Analysis")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = YouTubeSEOAnalyzer()
    
    # Analyze a video
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = analyzer.analyze_video(video_url)
    
    # Print basic info
    print(f"Title: {result['metadata']['title']}")
    print(f"Views: {result['metadata']['statistics']['view_count']:,}")
    print(f"Engagement Rate: {result['engagement']['engagement_rate']}%")
    print()


def example_sentiment_analysis():
    """Example: Sentiment analysis of comments"""
    print("Example 2: Sentiment Analysis")
    print("=" * 60)
    
    # Sample comments
    comments = [
        "This is amazing! Love this video!",
        "Very helpful, thank you!",
        "Not what I expected...",
        "Great content as always",
        "Could be better"
    ]
    
    # Analyze sentiment
    sentiment_analyzer = SentimentAnalyzer()
    result = sentiment_analyzer.analyze_comments(comments)
    
    print(f"Overall Sentiment: {result['overall_sentiment']}")
    print(f"Positive: {result['sentiment_percentages']['positive']}%")
    print(f"Negative: {result['sentiment_percentages']['negative']}%")
    print()


def example_recommendations():
    """Example: Generate recommendations"""
    print("Example 3: Generate Recommendations")
    print("=" * 60)
    
    # Sample analysis data
    analysis_data = {
        'metadata': {
            'video_id': 'example123',
            'title': 'How to Code in Python',
            'description': 'Learn Python basics',
            'tags': ['python', 'coding'],
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'statistics': {
                'view_count': 1000,
                'like_count': 50,
                'comment_count': 10
            },
            'channel_statistics': {
                'subscriber_count': 5000
            }
        },
        'engagement': {
            'engagement_rate': 6.0,
            'like_rate': 5.0,
            'comment_rate': 1.0,
            'estimated_ctr': 20.0
        },
        'top_videos': []
    }
    
    # Generate recommendations
    rec_engine = RecommendationEngine(api_key=None)  # No AI for this example
    recommendations = rec_engine.generate_recommendations(analysis_data)
    
    print("Title Optimization Score:", recommendations['title_optimization']['score'])
    print("Suggestions:")
    for suggestion in recommendations['title_optimization']['suggestions'][:3]:
        print(f"  • {suggestion}")
    print()


def example_comparison():
    """Example: Compare with top videos"""
    print("Example 4: Compare with Top Videos")
    print("=" * 60)
    
    analyzer = YouTubeSEOAnalyzer()
    
    # Search for top videos
    top_videos = analyzer.fetch_top_ranking_videos("python tutorial", max_results=3)
    
    if top_videos:
        print(f"Found {len(top_videos)} top videos:")
        for i, video in enumerate(top_videos, 1):
            print(f"{i}. {video['title'][:50]}...")
            print(f"   Views: {video['view_count']:,}")
    print()


def example_save_report():
    """Example: Save analysis to JSON"""
    print("Example 5: Save Report to JSON")
    print("=" * 60)
    
    # Create sample report
    report = {
        'video_id': 'example123',
        'title': 'Example Video',
        'analysis_date': '2024-01-15',
        'metrics': {
            'views': 1000,
            'engagement_rate': 5.0
        },
        'recommendations': [
            'Optimize title length',
            'Add more tags',
            'Improve thumbnail'
        ]
    }
    
    # Save to file
    filename = '/tmp/example_report.json'
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {filename}")
    print()


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("YouTube SEO Analyzer - Usage Examples")
    print("="*60 + "\n")
    
    try:
        # Run examples that don't require API keys
        example_sentiment_analysis()
        example_recommendations()
        example_save_report()
        
        print("\n" + "="*60)
        print("Examples Complete!")
        print("="*60)
        print("\nNote: Some examples require API keys to run fully.")
        print("Set YOUTUBE_API_KEY in .env to run all examples.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set up your API keys in .env file.")


if __name__ == "__main__":
    main()
