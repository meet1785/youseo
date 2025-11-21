#!/usr/bin/env python3
"""
YouTube SEO Analyzer - Command Line Interface
Main entry point for analyzing YouTube videos and generating SEO recommendations
"""

import sys
import os
import argparse
import json
from datetime import datetime
from youtube_analyzer import YouTubeSEOAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from recommendation_engine import RecommendationEngine
from batch_analyzer import BatchAnalyzer



def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🎥  YouTube SEO Analyzer & Optimizer  🎥            ║
    ║                                                               ║
    ║         AI-Powered Video Analysis & Recommendations          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_video_info(metadata):
    """Print basic video information"""
    print("\n" + "="*70)
    print("📹 VIDEO INFORMATION")
    print("="*70)
    print(f"Title: {metadata['title']}")
    print(f"Channel: {metadata['channel_title']}")
    print(f"Published: {metadata['published_at'][:10]}")
    print(f"Duration: {metadata['duration']}")
    print(f"Video ID: {metadata['video_id']}")
    print(f"Category: {metadata['category_id']}")


def print_statistics(metadata, engagement):
    """Print video statistics"""
    stats = metadata['statistics']
    
    print("\n" + "="*70)
    print("📊 STATISTICS & METRICS")
    print("="*70)
    print(f"Views: {stats['view_count']:,}")
    print(f"Likes: {stats['like_count']:,}")
    print(f"Comments: {stats['comment_count']:,}")
    print(f"\nEngagement Rate: {engagement['engagement_rate']}%")
    print(f"Like Rate: {engagement['like_rate']}%")
    print(f"Comment Rate: {engagement['comment_rate']}%")
    print(f"Estimated CTR: {engagement['estimated_ctr']}%")


def print_sentiment_analysis(sentiment_data):
    """Print sentiment analysis results"""
    if not sentiment_data or sentiment_data['total_comments'] == 0:
        print("\n⚠️  No comments available for sentiment analysis")
        return
    
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


def print_comparison(top_videos, current_views):
    """Print comparison with top-ranking videos"""
    if not top_videos:
        print("\n⚠️  No comparison data available")
        return
    
    print("\n" + "="*70)
    print("🏆 TOP VIDEOS IN NICHE (Comparison)")
    print("="*70)
    
    avg_views = sum(v['view_count'] for v in top_videos) / len(top_videos)
    print(f"Average Views of Top Videos: {int(avg_views):,}")
    print(f"Your Video Views: {current_views:,}")
    
    if current_views < avg_views:
        percentage = ((avg_views - current_views) / avg_views) * 100
        print(f"Gap: {percentage:.1f}% below average")
    else:
        percentage = ((current_views - avg_views) / avg_views) * 100
        print(f"Performance: {percentage:.1f}% above average! 🎉")
    
    print(f"\nTop {len(top_videos)} Videos:")
    for i, video in enumerate(top_videos[:5], 1):
        print(f"  {i}. {video['title'][:60]}...")
        print(f"     Views: {video['view_count']:,} | Likes: {video['like_count']:,}")


def save_detailed_report(analysis_data, recommendations, filename):
    """Save detailed analysis report to JSON file"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'video_info': {
            'video_id': analysis_data['metadata']['video_id'],
            'title': analysis_data['metadata']['title'],
            'channel': analysis_data['metadata']['channel_title'],
            'url': f"https://www.youtube.com/watch?v={analysis_data['metadata']['video_id']}"
        },
        'metadata': analysis_data['metadata'],
        'engagement': analysis_data['engagement'],
        'sentiment': analysis_data.get('sentiment', {}),
        'top_videos': analysis_data.get('top_videos', []),
        'recommendations': recommendations
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: {filename}")


def handle_batch_analysis(args):
    """Handle batch analysis of multiple videos"""
    print_banner()
    
    try:
        # Initialize analyzers
        print("🔧 Initializing analyzers...")
        use_cache = not args.no_cache
        youtube_analyzer = YouTubeSEOAnalyzer(use_cache=use_cache)
        sentiment_analyzer = SentimentAnalyzer()
        
        if use_cache:
            print("  ⚡ Cache enabled - API quota usage will be reduced")
        else:
            print("  ⚠️  Cache disabled - will use full API quota")
        
        if args.no_ai:
            print("⚠️  AI insights disabled")
            recommendation_engine = RecommendationEngine(api_key=None)
        else:
            recommendation_engine = RecommendationEngine()
        
        # Create batch analyzer
        batch_analyzer = BatchAnalyzer(
            youtube_analyzer,
            sentiment_analyzer,
            recommendation_engine
        )
        
        # Get URLs to analyze
        if args.batch:
            print(f"\n📂 Reading URLs from file: {args.batch}")
            urls = batch_analyzer.parse_urls_from_file(args.batch)
        else:
            urls = args.urls
        
        if not urls:
            print("❌ No URLs found to analyze")
            return 1
        
        print(f"Found {len(urls)} video(s) to analyze")
        
        # Analyze videos
        results = batch_analyzer.analyze_videos(
            urls,
            analyze_comments=not args.no_comments,
            max_comments=args.max_comments,
            use_ai=not args.no_ai
        )
        
        # Print summary report
        batch_analyzer.print_summary_report()
        
        # Export results
        if args.batch_output:
            output_file = args.batch_output
        else:
            output_file = f"batch_results.{args.batch_format}"
        batch_analyzer.export_results(output_file, args.batch_format)
        
        print("\n✅ Batch analysis complete!")
        print("\nNext Steps:")
        print("  1. Review the batch summary above")
        print(f"  2. Check detailed results in: {output_file}")
        print("  3. Focus on improving lowest-performing videos")
        print("  4. Apply insights from best-performing videos to others")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        print("Please check your API keys and internet connection.", file=sys.stderr)
        return 1


def main():
    """Main application function"""
    parser = argparse.ArgumentParser(
        description='YouTube SEO Analyzer - Analyze videos and get AI-powered recommendations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single video analysis
  python youseo.py https://www.youtube.com/watch?v=VIDEO_ID
  python youseo.py https://youtu.be/VIDEO_ID --output report.json
  python youseo.py https://www.youtube.com/shorts/VIDEO_ID --no-ai
  
  # Batch analysis
  python youseo.py --batch videos.txt --batch-output results.json
  python youseo.py --urls URL1 URL2 URL3 --batch-format csv
  
  # Cache management
  python youseo.py --cache-stats
  python youseo.py --cache-clear
        """
    )
    
    parser.add_argument(
        'video_url',
        nargs='?',
        help='YouTube video URL (supports regular videos and shorts)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Save detailed report to JSON file',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI-powered insights (useful if OpenAI API key is not set)'
    )
    
    parser.add_argument(
        '--no-comments',
        action='store_true',
        help='Skip comment sentiment analysis'
    )
    
    parser.add_argument(
        '--max-comments',
        type=int,
        default=100,
        help='Maximum number of comments to analyze (default: 100)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching for this analysis'
    )
    
    parser.add_argument(
        '--cache-stats',
        action='store_true',
        help='Show cache statistics and exit'
    )
    
    parser.add_argument(
        '--cache-clear',
        action='store_true',
        help='Clear all cached data and exit'
    )
    
    # Batch analysis options
    parser.add_argument(
        '--batch',
        metavar='FILE',
        help='Batch analyze videos from file (txt or csv)'
    )
    
    parser.add_argument(
        '--urls',
        nargs='+',
        metavar='URL',
        help='Batch analyze multiple video URLs'
    )
    
    parser.add_argument(
        '--batch-output',
        metavar='FILE',
        help='Output file for batch results (default: batch_results.json)'
    )
    
    parser.add_argument(
        '--batch-format',
        choices=['json', 'csv'],
        default='json',
        help='Batch output format: json or csv (default: json)'
    )
    
    args = parser.parse_args()
    
    # Handle cache management commands
    if args.cache_stats or args.cache_clear:
        from cache_manager import CacheManager
        import json as json_lib
        
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json_lib.load(f)
            cache_dir = config.get('cache_settings', {}).get('cache_directory', '.cache')
        except (FileNotFoundError, json_lib.JSONDecodeError, KeyError):
            cache_dir = '.cache'
        
        cache = CacheManager(cache_dir=cache_dir)
        
        if args.cache_stats:
            print("\n📊 Cache Statistics")
            print("=" * 70)
            stats = cache.get_stats()
            print(f"Cache Directory: {stats['cache_directory']}")
            print(f"Total Size: {stats['total_cache_size_mb']} MB")
            print(f"\nVideo Metadata:")
            print(f"  Total: {stats['video']['total']} | Valid: {stats['video']['valid']} | Expired: {stats['video']['expired']}")
            print(f"Comments:")
            print(f"  Total: {stats['comments']['total']} | Valid: {stats['comments']['valid']} | Expired: {stats['comments']['expired']}")
            print(f"Search Results:")
            print(f"  Total: {stats['search']['total']} | Valid: {stats['search']['valid']} | Expired: {stats['search']['expired']}")
            
            # Cleanup expired entries
            expired_count = cache.cleanup_expired()
            if expired_count > 0:
                print(f"\n🧹 Cleaned up {expired_count} expired cache entries")
            return 0
        
        if args.cache_clear:
            count = cache.clear()
            print(f"\n🗑️  Cleared {count} cache entries")
            return 0
    
    # Handle batch analysis
    if args.batch or args.urls:
        return handle_batch_analysis(args)
    
    # Require video URL for single video analysis
    if not args.video_url:
        parser.error("video_url is required for video analysis (or use --batch/--urls for batch analysis)")
    
    # Print banner
    print_banner()
    
    try:
        # Initialize analyzers
        print("🔧 Initializing analyzers...")
        use_cache = not args.no_cache
        youtube_analyzer = YouTubeSEOAnalyzer(use_cache=use_cache)
        sentiment_analyzer = SentimentAnalyzer()
        
        if use_cache:
            print("  ⚡ Cache enabled - API quota usage will be reduced")
        else:
            print("  ⚠️  Cache disabled - will use full API quota")
        
        if args.no_ai:
            print("⚠️  AI insights disabled")
            recommendation_engine = RecommendationEngine(api_key=None)
        else:
            recommendation_engine = RecommendationEngine()
        
        # Analyze video
        print(f"\n🔍 Analyzing video: {args.video_url}")
        print("-" * 70)
        
        analysis_data = youtube_analyzer.analyze_video(args.video_url)
        
        # Print video information
        print_video_info(analysis_data['metadata'])
        print_statistics(analysis_data['metadata'], analysis_data['engagement'])
        
        # Sentiment analysis
        if not args.no_comments:
            print("\n🧠 Analyzing comment sentiment...")
            sentiment_data = sentiment_analyzer.analyze_comments(analysis_data['comments'])
            analysis_data['sentiment'] = sentiment_data
            print_sentiment_analysis(sentiment_data)
        
        # Comparison with top videos
        print_comparison(
            analysis_data['top_videos'],
            analysis_data['metadata']['statistics']['view_count']
        )
        
        # Generate recommendations
        print("\n🤖 Generating SEO recommendations...")
        recommendations = recommendation_engine.generate_recommendations(analysis_data)
        
        # Print recommendations report
        report = recommendation_engine.generate_report(recommendations)
        print("\n" + report)
        
        # Save detailed report if requested
        if args.output:
            save_detailed_report(analysis_data, recommendations, args.output)
        
        print("\n✅ Analysis complete!")
        print("\nNext Steps:")
        print("  1. Review the recommendations above")
        print("  2. Implement suggested optimizations")
        print("  3. Monitor performance after changes")
        print("  4. Re-analyze after 1-2 weeks to track improvement")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        print("Please check your API keys and internet connection.", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
