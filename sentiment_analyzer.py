"""
Sentiment Analysis Module
Analyzes comments sentiment and extracts insights
"""

import re
from typing import List, Dict
from textblob import TextBlob
from collections import Counter


class SentimentAnalyzer:
    """Analyze sentiment of comments and feedback"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing HTML tags and extra whitespace"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a single text"""
        cleaned_text = self.clean_text(text)
        
        if not cleaned_text:
            return {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment': 'neutral'}
        
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
    
    def analyze_comments(self, comments: List[str]) -> Dict:
        """Analyze multiple comments and generate summary"""
        if not comments:
            return {
                'total_comments': 0,
                'sentiment_distribution': {
                    'positive': 0,
                    'neutral': 0,
                    'negative': 0
                },
                'average_polarity': 0.0,
                'average_subjectivity': 0.0,
                'overall_sentiment': 'neutral'
            }
        
        sentiments = []
        polarities = []
        subjectivities = []
        
        for comment in comments:
            result = self.analyze_sentiment(comment)
            sentiments.append(result['sentiment'])
            polarities.append(result['polarity'])
            subjectivities.append(result['subjectivity'])
        
        # Count sentiment distribution
        sentiment_counts = Counter(sentiments)
        total = len(sentiments)
        
        avg_polarity = sum(polarities) / total if total > 0 else 0
        avg_subjectivity = sum(subjectivities) / total if total > 0 else 0
        
        # Determine overall sentiment
        if avg_polarity > 0.1:
            overall = 'positive'
        elif avg_polarity < -0.1:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'total_comments': total,
            'sentiment_distribution': {
                'positive': sentiment_counts.get('positive', 0),
                'neutral': sentiment_counts.get('neutral', 0),
                'negative': sentiment_counts.get('negative', 0)
            },
            'sentiment_percentages': {
                'positive': round((sentiment_counts.get('positive', 0) / total) * 100, 1),
                'neutral': round((sentiment_counts.get('neutral', 0) / total) * 100, 1),
                'negative': round((sentiment_counts.get('negative', 0) / total) * 100, 1)
            },
            'average_polarity': round(avg_polarity, 3),
            'average_subjectivity': round(avg_subjectivity, 3),
            'overall_sentiment': overall
        }
    
    def extract_common_themes(self, comments: List[str], top_n: int = 10) -> List[tuple]:
        """Extract common words/themes from comments"""
        # Stop words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our',
            'their', 'me', 'him', 'us', 'them'
        }
        
        all_words = []
        for comment in comments:
            cleaned = self.clean_text(comment.lower())
            words = re.findall(r'\b\w+\b', cleaned)
            # Filter out stop words and short words
            words = [w for w in words if w not in stop_words and len(w) > 3]
            all_words.extend(words)
        
        # Count word frequencies
        word_counts = Counter(all_words)
        return word_counts.most_common(top_n)
