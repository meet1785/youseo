"""
AI Recommendation Engine
Generates SEO recommendations using AI analysis
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Optional OpenAI import
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()


class RecommendationEngine:
    """Generate AI-powered SEO recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize recommendation engine with OpenAI API"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_ai = bool(self.api_key) and OPENAI_AVAILABLE
        
        if self.use_ai and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_recommendations(self, analysis_data: Dict) -> Dict:
        """Generate comprehensive recommendations based on analysis"""
        metadata = analysis_data['metadata']
        engagement = analysis_data['engagement']
        top_videos = analysis_data.get('top_videos', [])
        sentiment = analysis_data.get('sentiment', {})
        
        recommendations = {
            'title_optimization': self._analyze_title(metadata, top_videos),
            'description_optimization': self._analyze_description(metadata, top_videos),
            'tags_optimization': self._analyze_tags(metadata, top_videos),
            'thumbnail_optimization': self._analyze_thumbnail(metadata),
            'engagement_strategies': self._analyze_engagement(engagement, sentiment),
            'seo_improvements': self._analyze_seo(metadata, top_videos),
            'content_suggestions': self._generate_content_suggestions(metadata, top_videos, engagement)
        }
        
        # If OpenAI is available, enhance recommendations with AI
        if self.use_ai:
            recommendations['ai_insights'] = self._get_ai_insights(analysis_data)
        
        return recommendations
    
    def _analyze_title(self, metadata: Dict, top_videos: List[Dict]) -> Dict:
        """Analyze and recommend title improvements"""
        title = metadata['title']
        title_length = len(title)
        
        suggestions = []
        score = 100
        
        # Check title length (optimal: 50-60 characters)
        if title_length < 30:
            suggestions.append("Title is too short. Aim for 50-60 characters for better SEO.")
            score -= 20
        elif title_length > 70:
            suggestions.append("Title is too long and may be truncated. Keep it under 70 characters.")
            score -= 10
        else:
            suggestions.append("✓ Title length is good!")
        
        # Check for numbers (increase CTR by ~36%)
        if not any(char.isdigit() for char in title):
            suggestions.append("Consider adding numbers (e.g., '5 Tips', '2024 Guide') to increase CTR.")
            score -= 15
        
        # Check for power words
        power_words = ['best', 'ultimate', 'complete', 'guide', 'tutorial', 'tips', 'secrets', 'how to']
        has_power_word = any(word in title.lower() for word in power_words)
        if not has_power_word:
            suggestions.append("Add power words like 'Ultimate', 'Complete', or 'Best' to attract clicks.")
            score -= 10
        
        # Compare with top videos
        if top_videos:
            avg_top_title_length = sum(len(v['title']) for v in top_videos) / len(top_videos)
            if abs(title_length - avg_top_title_length) > 20:
                suggestions.append(f"Top videos in your niche average {int(avg_top_title_length)} characters in titles.")
                score -= 5
        
        return {
            'current_title': title,
            'length': title_length,
            'score': max(score, 0),
            'suggestions': suggestions
        }
    
    def _analyze_description(self, metadata: Dict, top_videos: List[Dict]) -> Dict:
        """Analyze and recommend description improvements"""
        description = metadata['description']
        desc_length = len(description)
        
        suggestions = []
        score = 100
        
        # Check description length (optimal: 200+ characters)
        if desc_length < 100:
            suggestions.append("Description is too short. Aim for at least 200 characters with relevant keywords.")
            score -= 30
        elif desc_length < 200:
            suggestions.append("Description could be longer. Add more context and keywords.")
            score -= 15
        else:
            suggestions.append("✓ Description length is good!")
        
        # Check for timestamps (for longer videos)
        if 'timestamp' not in description.lower() and ':' not in description:
            suggestions.append("Consider adding timestamps to improve user experience and watch time.")
            score -= 10
        
        # Check for links
        if 'http' not in description and 'www' not in description:
            suggestions.append("Add relevant links (social media, resources) to increase engagement.")
            score -= 5
        
        # Check for keywords in first 200 characters
        first_200 = description[:200].lower()
        title_words = set(metadata['title'].lower().split())
        common_words = title_words.intersection(set(first_200.split()))
        if len(common_words) < 2:
            suggestions.append("Include key terms from your title in the first 200 characters of description.")
            score -= 10
        
        return {
            'current_length': desc_length,
            'score': max(score, 0),
            'suggestions': suggestions
        }
    
    def _analyze_tags(self, metadata: Dict, top_videos: List[Dict]) -> Dict:
        """Analyze and recommend tag improvements"""
        tags = metadata.get('tags', [])
        tag_count = len(tags)
        
        suggestions = []
        score = 100
        
        # Check number of tags (optimal: 5-8 highly relevant tags)
        if tag_count == 0:
            suggestions.append("No tags found! Add 5-8 relevant tags to improve discoverability.")
            score -= 40
        elif tag_count < 3:
            suggestions.append("Add more tags. Aim for 5-8 highly relevant tags.")
            score -= 20
        elif tag_count > 15:
            suggestions.append("Too many tags may dilute relevance. Focus on 5-8 most relevant tags.")
            score -= 10
        else:
            suggestions.append("✓ Good number of tags!")
        
        # Collect common tags from top videos
        if top_videos:
            all_top_tags = []
            for video in top_videos:
                all_top_tags.extend(video.get('tags', []))
            
            if all_top_tags:
                from collections import Counter
                common_tags = [tag for tag, count in Counter(all_top_tags).most_common(10)]
                missing_tags = [tag for tag in common_tags if tag.lower() not in [t.lower() for t in tags]]
                
                if missing_tags:
                    suggestions.append(f"Consider using these tags from top videos: {', '.join(missing_tags[:5])}")
                    score -= 15
        
        return {
            'current_tags': tags,
            'tag_count': tag_count,
            'score': max(score, 0),
            'suggestions': suggestions
        }
    
    def _analyze_thumbnail(self, metadata: Dict) -> Dict:
        """Analyze thumbnail and provide recommendations"""
        suggestions = [
            "Use high-contrast colors to stand out in search results",
            "Include human faces with clear emotions (increases CTR by 35%)",
            "Add bold, readable text (3-5 words maximum)",
            "Ensure thumbnail is clear even at small sizes",
            "Use consistent branding across thumbnails",
            "Avoid clickbait that doesn't match content",
            "Test different thumbnail designs with A/B testing"
        ]
        
        return {
            'thumbnail_url': metadata['thumbnail_url'],
            'suggestions': suggestions,
            'score': 75  # Default score as we can't analyze image programmatically
        }
    
    def _analyze_engagement(self, engagement: Dict, sentiment: Dict) -> Dict:
        """Analyze engagement metrics and provide strategies"""
        suggestions = []
        score = 100
        
        engagement_rate = engagement['engagement_rate']
        like_rate = engagement['like_rate']
        comment_rate = engagement['comment_rate']
        
        # Analyze engagement rate (good: >4%)
        if engagement_rate < 2:
            suggestions.append("Low engagement rate. Create compelling CTAs and ask questions to encourage interaction.")
            score -= 30
        elif engagement_rate < 4:
            suggestions.append("Moderate engagement. Improve by asking viewers to like, comment, and subscribe.")
            score -= 15
        else:
            suggestions.append("✓ Excellent engagement rate!")
        
        # Analyze like rate
        if like_rate < 1:
            suggestions.append("Low like rate. Remind viewers to like if they found the content valuable.")
            score -= 20
        
        # Analyze comment rate
        if comment_rate < 0.5:
            suggestions.append("Low comment rate. Ask engaging questions and respond to comments to build community.")
            score -= 15
        
        # Sentiment analysis
        if sentiment and sentiment.get('overall_sentiment') == 'negative':
            suggestions.append("⚠ Negative sentiment detected. Review feedback and address concerns in future content.")
            score -= 20
        elif sentiment and sentiment.get('overall_sentiment') == 'positive':
            suggestions.append("✓ Positive sentiment! Keep delivering value and engaging with your audience.")
        
        return {
            'engagement_rate': engagement_rate,
            'score': max(score, 0),
            'suggestions': suggestions
        }
    
    def _analyze_seo(self, metadata: Dict, top_videos: List[Dict]) -> Dict:
        """Analyze SEO factors and provide improvements"""
        suggestions = []
        score = 100
        
        # Check video stats compared to top performers
        if top_videos:
            avg_views = sum(v['view_count'] for v in top_videos) / len(top_videos)
            current_views = metadata['statistics']['view_count']
            
            if current_views < avg_views * 0.5:
                suggestions.append(f"Views below niche average. Focus on SEO optimization and promotion.")
                score -= 20
        
        # General SEO tips
        suggestions.extend([
            "Post consistently (at least once a week) to maintain channel momentum",
            "Optimize video for watch time - hook viewers in first 15 seconds",
            "Use cards and end screens to keep viewers on your channel",
            "Create playlists to organize content and increase session time",
            "Promote video on social media and relevant communities",
            "Engage with comments within first hour of posting",
            "Use hashtags (3-5 relevant ones) in description",
            "Consider video length - 7-15 minutes often perform best"
        ])
        
        return {
            'score': max(score, 0),
            'suggestions': suggestions
        }
    
    def _generate_content_suggestions(self, metadata: Dict, top_videos: List[Dict], engagement: Dict) -> Dict:
        """Generate content improvement suggestions"""
        suggestions = []
        
        # Based on engagement
        if engagement['estimated_ctr'] < 5:
            suggestions.append("Improve thumbnail and title to increase CTR")
        
        # Based on top videos
        if top_videos:
            avg_views = sum(v['view_count'] for v in top_videos) / len(top_videos)
            suggestions.append(f"Top videos in your niche average {int(avg_views):,} views")
            suggestions.append("Study top performers' content structure and topics")
        
        # General content suggestions
        suggestions.extend([
            "Create content that solves specific problems",
            "Use storytelling techniques to maintain interest",
            "Include clear value proposition in first 30 seconds",
            "End with strong CTA (subscribe, watch next video)",
            "Consider creating series or multi-part content",
            "Collaborate with other creators in your niche"
        ])
        
        return {
            'suggestions': suggestions
        }
    
    def _get_ai_insights(self, analysis_data: Dict) -> Dict:
        """Get AI-powered insights using OpenAI"""
        try:
            metadata = analysis_data['metadata']
            engagement = analysis_data['engagement']
            
            prompt = f"""As a YouTube SEO expert, analyze this video and provide specific, actionable recommendations:

Video Title: {metadata['title']}
Description: {metadata['description'][:200]}...
Tags: {', '.join(metadata.get('tags', [])[:10])}
Views: {metadata['statistics']['view_count']:,}
Engagement Rate: {engagement['engagement_rate']}%
Like Rate: {engagement['like_rate']}%

Provide 5 specific, prioritized recommendations to improve this video's performance."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert YouTube SEO consultant with deep knowledge of the platform's algorithm and best practices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_recommendations = response.choices[0].message.content
            
            return {
                'enabled': True,
                'recommendations': ai_recommendations
            }
            
        except Exception as e:
            return {
                'enabled': False,
                'error': f"AI insights unavailable: {str(e)}"
            }
    
    def generate_report(self, recommendations: Dict) -> str:
        """Generate a formatted report from recommendations"""
        report = []
        report.append("=" * 60)
        report.append("YOUTUBE SEO ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Title optimization
        report.append("\n📝 TITLE OPTIMIZATION")
        report.append("-" * 60)
        title_rec = recommendations['title_optimization']
        report.append(f"Current: {title_rec['current_title']}")
        report.append(f"Length: {title_rec['length']} characters")
        report.append(f"Score: {title_rec['score']}/100")
        report.append("\nSuggestions:")
        for suggestion in title_rec['suggestions']:
            report.append(f"  • {suggestion}")
        
        # Description optimization
        report.append("\n📄 DESCRIPTION OPTIMIZATION")
        report.append("-" * 60)
        desc_rec = recommendations['description_optimization']
        report.append(f"Length: {desc_rec['current_length']} characters")
        report.append(f"Score: {desc_rec['score']}/100")
        report.append("\nSuggestions:")
        for suggestion in desc_rec['suggestions']:
            report.append(f"  • {suggestion}")
        
        # Tags optimization
        report.append("\n🏷️  TAGS OPTIMIZATION")
        report.append("-" * 60)
        tags_rec = recommendations['tags_optimization']
        report.append(f"Current Tags: {tags_rec['tag_count']}")
        report.append(f"Score: {tags_rec['score']}/100")
        report.append("\nSuggestions:")
        for suggestion in tags_rec['suggestions']:
            report.append(f"  • {suggestion}")
        
        # Engagement strategies
        report.append("\n💬 ENGAGEMENT STRATEGIES")
        report.append("-" * 60)
        eng_rec = recommendations['engagement_strategies']
        report.append(f"Engagement Rate: {eng_rec['engagement_rate']}%")
        report.append(f"Score: {eng_rec['score']}/100")
        report.append("\nSuggestions:")
        for suggestion in eng_rec['suggestions']:
            report.append(f"  • {suggestion}")
        
        # SEO improvements
        report.append("\n🔍 SEO IMPROVEMENTS")
        report.append("-" * 60)
        seo_rec = recommendations['seo_improvements']
        report.append(f"Score: {seo_rec['score']}/100")
        report.append("\nKey Recommendations:")
        for i, suggestion in enumerate(seo_rec['suggestions'][:8], 1):
            report.append(f"  {i}. {suggestion}")
        
        # AI insights
        if 'ai_insights' in recommendations and recommendations['ai_insights'].get('enabled'):
            report.append("\n🤖 AI-POWERED INSIGHTS")
            report.append("-" * 60)
            report.append(recommendations['ai_insights']['recommendations'])
        
        report.append("\n" + "=" * 60)
        report.append("End of Report")
        report.append("=" * 60)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test the recommendation engine
    print("Recommendation Engine Module")
