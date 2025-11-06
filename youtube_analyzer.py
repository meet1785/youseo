"""
YouTube SEO Analyzer - Main Module
Analyzes YouTube videos and provides SEO recommendations
"""

import os
import re
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
MIN_CHANNEL_SUBSCRIBERS_FOR_CTR = 1000  # Minimum subscriber count for CTR calculation


class YouTubeSEOAnalyzer:
    """Main class for analyzing YouTube videos and providing SEO recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the analyzer with YouTube API key"""
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY environment variable.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        # Handle various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Try parsing as query parameter
        try:
            parsed_url = urlparse(url)
            if parsed_url.hostname in ['youtube.com', 'www.youtube.com']:
                query_params = parse_qs(parsed_url.query)
                if 'v' in query_params:
                    return query_params['v'][0]
        except Exception:
            pass
        
        return None
    
    def fetch_video_metadata(self, video_id: str) -> Dict:
        """Fetch comprehensive metadata for a YouTube video"""
        try:
            # Fetch video details
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,status',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                raise ValueError(f"Video not found: {video_id}")
            
            video_data = video_response['items'][0]
            snippet = video_data.get('snippet', {})
            statistics = video_data.get('statistics', {})
            content_details = video_data.get('contentDetails', {})
            
            # Fetch channel details
            channel_id = snippet.get('channelId')
            channel_response = self.youtube.channels().list(
                part='statistics,snippet',
                id=channel_id
            ).execute()
            
            channel_data = channel_response['items'][0] if channel_response.get('items') else {}
            channel_stats = channel_data.get('statistics', {})
            
            metadata = {
                'video_id': video_id,
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'tags': snippet.get('tags', []),
                'category_id': snippet.get('categoryId', ''),
                'published_at': snippet.get('publishedAt', ''),
                'channel_id': channel_id,
                'channel_title': snippet.get('channelTitle', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'duration': content_details.get('duration', ''),
                'statistics': {
                    'view_count': int(statistics.get('viewCount', 0)),
                    'like_count': int(statistics.get('likeCount', 0)),
                    'comment_count': int(statistics.get('commentCount', 0)),
                    'favorite_count': int(statistics.get('favoriteCount', 0))
                },
                'channel_statistics': {
                    'subscriber_count': int(channel_stats.get('subscriberCount', 0)),
                    'video_count': int(channel_stats.get('videoCount', 0)),
                    'view_count': int(channel_stats.get('viewCount', 0))
                }
            }
            
            return metadata
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {str(e)}")
    
    def calculate_engagement_metrics(self, metadata: Dict) -> Dict:
        """Calculate engagement metrics from video statistics"""
        stats = metadata['statistics']
        views = stats['view_count']
        
        if views == 0:
            return {
                'engagement_rate': 0.0,
                'like_rate': 0.0,
                'comment_rate': 0.0,
                'estimated_ctr': 0.0
            }
        
        likes = stats['like_count']
        comments = stats['comment_count']
        
        # Calculate engagement metrics
        engagement_rate = ((likes + comments) / views) * 100
        like_rate = (likes / views) * 100
        comment_rate = (comments / views) * 100
        
        # Estimate CTR based on views and channel size
        channel_subs = metadata['channel_statistics']['subscriber_count']
        estimated_ctr = min((views / max(channel_subs, MIN_CHANNEL_SUBSCRIBERS_FOR_CTR)) * 100, 100)
        
        return {
            'engagement_rate': round(engagement_rate, 2),
            'like_rate': round(like_rate, 2),
            'comment_rate': round(comment_rate, 2),
            'estimated_ctr': round(estimated_ctr, 2)
        }
    
    def fetch_top_ranking_videos(self, search_query: str, max_results: int = 5) -> List[Dict]:
        """Fetch top-ranking videos in the same niche"""
        try:
            search_response = self.youtube.search().list(
                q=search_query,
                type='video',
                part='id,snippet',
                order='viewCount',
                maxResults=max_results
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            # Fetch full details for these videos
            videos_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            top_videos = []
            for video in videos_response.get('items', []):
                snippet = video.get('snippet', {})
                statistics = video.get('statistics', {})
                
                top_videos.append({
                    'video_id': video['id'],
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'tags': snippet.get('tags', []),
                    'view_count': int(statistics.get('viewCount', 0)),
                    'like_count': int(statistics.get('likeCount', 0)),
                    'comment_count': int(statistics.get('commentCount', 0))
                })
            
            return top_videos
            
        except HttpError as e:
            print(f"Error fetching top videos: {str(e)}")
            return []
    
    def fetch_video_comments(self, video_id: str, max_results: int = 100) -> List[str]:
        """Fetch comments from a video for sentiment analysis"""
        try:
            comments = []
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_results, 100),
                order='relevance'
            )
            
            response = request.execute()
            
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            
            return comments
            
        except HttpError as e:
            print(f"Comments disabled or error: {str(e)}")
            return []
    
    def analyze_video(self, video_url: str) -> Dict:
        """Complete analysis of a YouTube video"""
        # Extract video ID
        video_id = self.extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {video_url}")
        
        print(f"Analyzing video: {video_id}")
        
        # Fetch metadata
        metadata = self.fetch_video_metadata(video_id)
        print(f"✓ Fetched metadata for: {metadata['title']}")
        
        # Calculate engagement metrics
        engagement = self.calculate_engagement_metrics(metadata)
        print(f"✓ Calculated engagement metrics")
        
        # Fetch comments for sentiment analysis
        comments = self.fetch_video_comments(video_id)
        print(f"✓ Fetched {len(comments)} comments")
        
        # Search for top videos in the same niche
        search_query = metadata['title'][:50]  # Use first 50 chars of title
        top_videos = self.fetch_top_ranking_videos(search_query)
        print(f"✓ Found {len(top_videos)} top-ranking videos in niche")
        
        return {
            'metadata': metadata,
            'engagement': engagement,
            'comments': comments,
            'top_videos': top_videos
        }


def main():
    """Main function for testing"""
    analyzer = YouTubeSEOAnalyzer()
    
    # Example usage
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = analyzer.analyze_video(test_url)
    
    print("\n" + "="*50)
    print("VIDEO ANALYSIS RESULTS")
    print("="*50)
    print(f"\nTitle: {result['metadata']['title']}")
    print(f"Views: {result['metadata']['statistics']['view_count']:,}")
    print(f"Engagement Rate: {result['engagement']['engagement_rate']}%")
    print(f"Estimated CTR: {result['engagement']['estimated_ctr']}%")
    print(f"\nTop Videos in Niche: {len(result['top_videos'])}")


if __name__ == "__main__":
    main()
