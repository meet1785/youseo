"""
Batch Analyzer Module
Enables analysis of multiple YouTube videos in a single run with comparative reporting
"""

import os
import csv
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class BatchAnalyzer:
    """Handles batch analysis of multiple YouTube videos"""
    
    def __init__(self, youtube_analyzer, sentiment_analyzer, recommendation_engine):
        """
        Initialize batch analyzer with required analyzers
        
        Args:
            youtube_analyzer: YouTubeSEOAnalyzer instance
            sentiment_analyzer: SentimentAnalyzer instance
            recommendation_engine: RecommendationEngine instance
        """
        self.youtube_analyzer = youtube_analyzer
        self.sentiment_analyzer = sentiment_analyzer
        self.recommendation_engine = recommendation_engine
        self.results = []
    
    def parse_urls_from_file(self, file_path: str) -> List[str]:
        """
        Parse video URLs from a file
        Supports .txt (one URL per line) and .csv (URL in first column)
        
        Args:
            file_path: Path to file containing URLs
            
        Returns:
            List of video URLs
        """
        urls = []
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type
        if file_path.suffix.lower() == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Skip header if present
                first_row = next(reader, None)
                if first_row and not first_row[0].startswith('http'):
                    # First row is header, continue with next rows
                    pass
                elif first_row:
                    # First row contains URL
                    urls.append(first_row[0].strip())
                
                for row in reader:
                    if row and row[0].strip():
                        urls.append(row[0].strip())
        else:
            # Assume .txt or plain text file
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    # Skip empty lines and comments
                    if url and not url.startswith('#'):
                        urls.append(url)
        
        return urls
    
    def analyze_videos(self, urls: List[str], analyze_comments: bool = True,
                      max_comments: int = 100, use_ai: bool = True) -> List[Dict]:
        """
        Analyze multiple videos and collect results
        
        Args:
            urls: List of video URLs to analyze
            analyze_comments: Whether to analyze comment sentiment
            max_comments: Maximum comments to analyze per video
            use_ai: Whether to use AI insights
            
        Returns:
            List of analysis results for each video
        """
        self.results = []
        total_videos = len(urls)
        
        print(f"\n🎬 Starting batch analysis of {total_videos} videos...")
        print("=" * 70)
        
        for idx, url in enumerate(urls, 1):
            print(f"\n[{idx}/{total_videos}] Analyzing: {url}")
            
            try:
                # Extract video ID
                video_id = self.youtube_analyzer.extract_video_id(url)
                if not video_id:
                    print(f"  ❌ Invalid URL, skipping...")
                    continue
                
                # Analyze video
                analysis_data = self.youtube_analyzer.analyze_video(url)
                
                # Sentiment analysis
                if analyze_comments:
                    sentiment_data = self.sentiment_analyzer.analyze_comments(
                        analysis_data['comments'][:max_comments]
                    )
                    analysis_data['sentiment'] = sentiment_data
                
                # Generate recommendations
                recommendations = self.recommendation_engine.generate_recommendations(
                    analysis_data
                )
                
                # Store result
                result = {
                    'url': url,
                    'video_id': video_id,
                    'analysis_data': analysis_data,
                    'recommendations': recommendations,
                    'analyzed_at': datetime.now().isoformat()
                }
                
                self.results.append(result)
                
                print(f"  ✅ Complete - {analysis_data['metadata']['title'][:50]}...")
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                # Continue with next video
                continue
        
        print("\n" + "=" * 70)
        print(f"✅ Batch analysis complete: {len(self.results)}/{total_videos} videos analyzed")
        
        return self.results
    
    def generate_summary(self) -> Dict:
        """
        Generate summary statistics and insights from batch results
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.results:
            return {'error': 'No results to summarize'}
        
        # Collect metrics
        view_counts = []
        engagement_rates = []
        like_rates = []
        titles = []
        
        for result in self.results:
            metadata = result['analysis_data']['metadata']
            engagement = result['analysis_data']['engagement']
            
            view_counts.append(metadata['statistics']['view_count'])
            engagement_rates.append(engagement['engagement_rate'])
            like_rates.append(engagement['like_rate'])
            titles.append({
                'title': metadata['title'],
                'views': metadata['statistics']['view_count'],
                'engagement': engagement['engagement_rate'],
                'url': result['url']
            })
        
        # Calculate statistics
        summary = {
            'total_videos': len(self.results),
            'total_views': sum(view_counts),
            'average_views': sum(view_counts) / len(view_counts) if view_counts else 0,
            'average_engagement_rate': sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0,
            'average_like_rate': sum(like_rates) / len(like_rates) if like_rates else 0,
            'best_performing': max(titles, key=lambda x: x['views']) if titles else None,
            'worst_performing': min(titles, key=lambda x: x['views']) if titles else None,
            'highest_engagement': max(titles, key=lambda x: x['engagement']) if titles else None,
            'lowest_engagement': min(titles, key=lambda x: x['engagement']) if titles else None,
        }
        
        return summary
    
    def export_results(self, output_file: str, format: str = 'json'):
        """
        Export batch results to file
        
        Args:
            output_file: Path to output file
            format: Export format ('json' or 'csv')
        """
        if not self.results:
            print("⚠️  No results to export")
            return
        
        if format.lower() == 'json':
            self._export_json(output_file)
        elif format.lower() == 'csv':
            self._export_csv(output_file)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, output_file: str):
        """Export results as JSON"""
        summary = self.generate_summary()
        
        export_data = {
            'summary': summary,
            'analyzed_at': datetime.now().isoformat(),
            'videos': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Batch results exported to: {output_file}")
    
    def _export_csv(self, output_file: str):
        """Export summary as CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'title', 'url', 'views', 'likes', 'comments',
                'engagement_rate', 'like_rate', 'overall_sentiment',
                'title_score', 'description_score', 'tags_score'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                metadata = result['analysis_data']['metadata']
                engagement = result['analysis_data']['engagement']
                sentiment = result['analysis_data'].get('sentiment', {})
                recommendations = result['recommendations']
                
                row = {
                    'title': metadata['title'],
                    'url': result['url'],
                    'views': metadata['statistics']['view_count'],
                    'likes': metadata['statistics']['like_count'],
                    'comments': metadata['statistics']['comment_count'],
                    'engagement_rate': engagement['engagement_rate'],
                    'like_rate': engagement['like_rate'],
                    'overall_sentiment': sentiment.get('overall_sentiment', 'N/A'),
                    'title_score': recommendations['title_optimization']['score'],
                    'description_score': recommendations['description_optimization']['score'],
                    'tags_score': recommendations['tags_optimization']['score']
                }
                writer.writerow(row)
        
        print(f"\n💾 Batch summary exported to: {output_file}")
    
    def print_summary_report(self):
        """Print a formatted summary report to console"""
        summary = self.generate_summary()
        
        if 'error' in summary:
            print(f"\n⚠️  {summary['error']}")
            return
        
        print("\n" + "=" * 70)
        print("📊 BATCH ANALYSIS SUMMARY")
        print("=" * 70)
        
        print(f"\nTotal Videos Analyzed: {summary['total_videos']}")
        print(f"Total Views: {summary['total_views']:,}")
        print(f"Average Views per Video: {summary['average_views']:,.0f}")
        print(f"Average Engagement Rate: {summary['average_engagement_rate']:.2f}%")
        print(f"Average Like Rate: {summary['average_like_rate']:.2f}%")
        
        if summary['best_performing']:
            print("\n🏆 Best Performing Video (by views):")
            print(f"  Title: {summary['best_performing']['title']}")
            print(f"  Views: {summary['best_performing']['views']:,}")
            print(f"  URL: {summary['best_performing']['url']}")
        
        if summary['worst_performing']:
            print("\n📉 Needs Improvement (lowest views):")
            print(f"  Title: {summary['worst_performing']['title']}")
            print(f"  Views: {summary['worst_performing']['views']:,}")
            print(f"  URL: {summary['worst_performing']['url']}")
        
        if summary['highest_engagement']:
            print("\n💬 Highest Engagement:")
            print(f"  Title: {summary['highest_engagement']['title']}")
            print(f"  Engagement Rate: {summary['highest_engagement']['engagement']:.2f}%")
            print(f"  URL: {summary['highest_engagement']['url']}")
        
        if summary['lowest_engagement']:
            print("\n😴 Lowest Engagement:")
            print(f"  Title: {summary['lowest_engagement']['title']}")
            print(f"  Engagement Rate: {summary['lowest_engagement']['engagement']:.2f}%")
            print(f"  URL: {summary['lowest_engagement']['url']}")
        
        print("\n" + "=" * 70)
