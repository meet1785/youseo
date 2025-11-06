# YouTube SEO Analyzer - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Understanding Reports](#understanding-reports)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/meet1785/youseo.git
cd youseo
```

### Step 2: Install Dependencies
```bash
# Option 1: Automatic setup (recommended)
chmod +x setup.sh
./setup.sh

# Option 2: Manual installation
pip install -r requirements.txt
```

### Step 3: Set Up API Keys
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

## Configuration

### Required API Keys

#### YouTube Data API v3 Key
The YouTube API key is **required** for all functionality.

**How to get it:**
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Library"
4. Search for "YouTube Data API v3" and enable it
5. Go to "Credentials" > "Create Credentials" > "API Key"
6. Copy the API key to your `.env` file

**Important Notes:**
- Free tier includes 10,000 quota units per day
- Each video analysis uses approximately 100-200 units
- Monitor your usage in Google Cloud Console

#### OpenAI API Key (Optional)
The OpenAI API key is **optional** and only used for AI-powered insights.

**How to get it:**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API keys section
3. Create a new API key
4. Copy the key to your `.env` file

**Cost:** Approximately $0.01-0.02 per video analysis (using GPT-3.5-turbo)

## Basic Usage

### Analyze a YouTube Video
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Analyze a YouTube Short
```bash
python youseo.py https://www.youtube.com/shorts/VIDEO_ID
```

### Save Report to File
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --output report.json
```

### Skip AI Insights
If you don't have an OpenAI API key or want to save costs:
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --no-ai
```

### Skip Comment Analysis
For faster analysis without sentiment data:
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --no-comments
```

### Limit Comment Analysis
Analyze fewer comments for faster processing:
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --max-comments 50
```

## Advanced Features

### Batch Analysis
Create a script to analyze multiple videos:

```python
#!/usr/bin/env python3
from youtube_analyzer import YouTubeSEOAnalyzer
from recommendation_engine import RecommendationEngine
import json

# List of video URLs
videos = [
    "https://www.youtube.com/watch?v=VIDEO_ID_1",
    "https://www.youtube.com/watch?v=VIDEO_ID_2",
    "https://www.youtube.com/watch?v=VIDEO_ID_3"
]

analyzer = YouTubeSEOAnalyzer()
rec_engine = RecommendationEngine()

results = []
for url in videos:
    try:
        analysis = analyzer.analyze_video(url)
        recs = rec_engine.generate_recommendations(analysis)
        results.append({
            'url': url,
            'title': analysis['metadata']['title'],
            'recommendations': recs
        })
    except Exception as e:
        print(f"Error analyzing {url}: {e}")

# Save all results
with open('batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Programmatic Usage
Use the analyzer in your own Python scripts:

```python
from youtube_analyzer import YouTubeSEOAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from recommendation_engine import RecommendationEngine

# Initialize
youtube_analyzer = YouTubeSEOAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
rec_engine = RecommendationEngine()

# Analyze video
analysis = youtube_analyzer.analyze_video(video_url)

# Get sentiment
sentiment = sentiment_analyzer.analyze_comments(analysis['comments'])

# Generate recommendations
analysis['sentiment'] = sentiment
recommendations = rec_engine.generate_recommendations(analysis)

# Generate report
report = rec_engine.generate_report(recommendations)
print(report)
```

## Understanding Reports

### Video Information Section
```
📹 VIDEO INFORMATION
Title: [Video Title]
Channel: [Channel Name]
Published: [Date]
Views: [View Count]
```
Basic metadata about the video.

### Statistics & Metrics
```
📊 STATISTICS & METRICS
Views: 10,000
Likes: 500
Comments: 100
Engagement Rate: 6.0%
Like Rate: 5.0%
Comment Rate: 1.0%
Estimated CTR: 2.5%
```

**Metrics Explained:**
- **Engagement Rate**: (Likes + Comments) / Views × 100
  - Good: >4%, Excellent: >8%
- **Like Rate**: Likes / Views × 100
  - Good: >2%, Excellent: >5%
- **Comment Rate**: Comments / Views × 100
  - Good: >0.5%, Excellent: >1%
- **Estimated CTR**: Views / Subscriber Count × 100
  - This is an estimate; actual CTR is only visible to creators

### Sentiment Analysis
```
💭 SENTIMENT ANALYSIS
Overall Sentiment: POSITIVE
Positive: 70%
Neutral: 20%
Negative: 10%
```

Analyzes up to 100 most relevant comments to gauge audience reaction.

### Title Optimization
```
📝 TITLE OPTIMIZATION
Score: 75/100
Suggestions:
  • Title length is good!
  • Consider adding numbers
  • Add power words
```

**Scoring Factors:**
- Length (50-60 characters optimal)
- Numbers presence
- Power words usage
- Comparison with top videos

### Description Optimization
```
📄 DESCRIPTION OPTIMIZATION
Score: 60/100
Suggestions:
  • Add more detail (aim for 200+ characters)
  • Include timestamps
  • Add relevant links
```

### Tags Optimization
```
🏷️ TAGS OPTIMIZATION
Score: 80/100
Current Tags: 5
Suggestions:
  • Good number of tags!
  • Consider these from top videos: [suggestions]
```

### SEO Improvements
General recommendations for improving video discoverability and performance.

## Best Practices

### For Best Results

1. **Analyze Competitor Videos First**
   - Find top-ranking videos in your niche
   - Note common patterns in titles, tags, thumbnails
   - Use insights to optimize your own videos

2. **Implement Recommendations Gradually**
   - Don't change everything at once
   - Test one change at a time
   - Monitor results after each change

3. **Re-analyze Periodically**
   - Check your video 24 hours after publishing
   - Re-analyze after 1 week
   - Track improvement over time

4. **Compare With Your Best Performers**
   - Analyze your most successful videos
   - Identify patterns that work for your audience
   - Replicate successful strategies

5. **Monitor Sentiment**
   - Read actual comments, not just sentiment scores
   - Address negative feedback
   - Engage with your audience

### Optimization Priorities

Focus on these in order:
1. **Title** - First impression, highest impact on CTR
2. **Thumbnail** - Works with title to drive clicks
3. **First 30 seconds** - Crucial for retention
4. **Description** - SEO and context
5. **Tags** - Discoverability
6. **Engagement** - Likes, comments, shares

## Troubleshooting

### Common Issues

#### "YouTube API key is required"
**Solution:** 
- Ensure `.env` file exists in the project directory
- Check that `YOUTUBE_API_KEY` is set correctly
- Verify the key is valid in Google Cloud Console

#### "Video not found"
**Possible causes:**
- Video is private or unlisted
- Video has been deleted
- Invalid URL format

**Solution:**
- Verify the video is public
- Check the URL is correct
- Try a different video

#### "Comments disabled or error"
**Note:** This is normal for videos with disabled comments.

**Solution:**
- Use `--no-comments` flag to skip sentiment analysis
- The tool will continue with other analyses

#### "Rate limit exceeded"
**Cause:** Too many API requests

**Solution:**
- Wait a few minutes before trying again
- Reduce the number of videos analyzed
- Check your quota usage in Google Cloud Console

#### "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

#### "AI insights unavailable"
**Causes:**
- OpenAI API key not set
- Invalid API key
- No credits in OpenAI account

**Solution:**
- Add valid `OPENAI_API_KEY` to `.env`
- Or use `--no-ai` flag to skip AI insights

### Performance Tips

1. **Reduce comment analysis:**
   ```bash
   python youseo.py URL --max-comments 50
   ```

2. **Skip AI insights for faster analysis:**
   ```bash
   python youseo.py URL --no-ai
   ```

3. **Analyze during off-peak hours** to avoid rate limits

## Example Workflows

### Workflow 1: New Video Launch
1. Create your video content
2. Draft title, description, tags
3. Run analyzer on similar successful videos
4. Refine your metadata based on recommendations
5. Publish with optimized metadata
6. Analyze your video 24 hours after publishing
7. Make adjustments if needed

### Workflow 2: Optimize Existing Video
1. Run analyzer on your video
2. Review all recommendations
3. Implement high-priority changes (title, thumbnail)
4. Update description and tags
5. Re-analyze after 1 week
6. Compare before/after metrics

### Workflow 3: Competitive Research
1. Find top 10 videos in your niche
2. Analyze each one
3. Save all reports
4. Identify common patterns
5. Create content strategy based on insights

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check README.md for updates
- **Examples**: Run `python examples.py` for code samples

---

**Note:** This tool provides recommendations based on best practices and data analysis. Results may vary depending on your specific niche, audience, and content quality. Always test and measure the impact of changes.
