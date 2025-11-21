# 🎥 YouTube SEO Analyzer

An AI-powered YouTube SEO analysis tool that helps content creators optimize their videos for maximum reach, engagement, and watch-time. Automatically fetches video metadata, analyzes performance metrics, compares with top-ranking videos, and provides actionable recommendations.

## ✨ Features

- **🔍 Automatic Metadata Extraction**: Fetches title, description, tags, thumbnail, and statistics
- **📊 Performance Analytics**: Analyzes CTR, engagement rate, like rate, and comment rate
- **💭 Sentiment Analysis**: Evaluates comment sentiment to understand audience feedback
- **🏆 Competitive Analysis**: Compares your video with top-ranking videos in the same niche
- **🤖 AI-Powered Recommendations**: Generates specific, actionable SEO improvements
- **📱 Supports All Video Types**: Works with regular videos and YouTube Shorts
- **🎬 Batch Analysis**: Analyze multiple videos at once with comparative insights
- **📈 Comprehensive Reporting**: Detailed JSON/CSV reports for tracking improvements
- **⚡ Intelligent Caching**: Reduces API quota usage by caching responses with configurable TTL

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- YouTube Data API v3 key
- OpenAI API key (optional, for AI insights)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/meet1785/youseo.git
cd youseo
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

#### Getting API Keys

**YouTube Data API v3:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

**OpenAI API (Optional):**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate an API key
3. Copy the API key to your `.env` file

### Usage

**Basic analysis:**
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID
```

**Save detailed report:**
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --output report.json
```

**Analyze YouTube Short:**
```bash
python youseo.py https://www.youtube.com/shorts/VIDEO_ID
```

**Skip AI insights (if OpenAI key not available):**
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --no-ai
```

**Skip comment analysis:**
```bash
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --no-comments
```

**Batch analysis from file:**
```bash
# Analyze multiple videos from a text file (one URL per line)
python youseo.py --batch videos.txt --batch-output results.json

# Export batch results as CSV
python youseo.py --batch videos.txt --batch-format csv
```

**Batch analysis from command line:**
```bash
# Analyze multiple videos directly from command line
python youseo.py --urls URL1 URL2 URL3 --batch-output results.json
```

**Cache management:**
```bash
# View cache statistics
python youseo.py --cache-stats

# Clear all cached data
python youseo.py --cache-clear

# Disable cache for a single analysis
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID --no-cache
```

## 📊 What Gets Analyzed

### Video Metadata
- Title, description, tags
- Thumbnail URL
- Duration, publish date
- Category and channel info

### Performance Metrics
- View count, likes, comments
- Engagement rate (likes + comments / views)
- Like rate (likes / views)
- Comment rate (comments / views)
- Estimated CTR based on channel size

### Sentiment Analysis
- Overall sentiment (positive/neutral/negative)
- Sentiment distribution
- Average polarity and subjectivity
- Common themes in comments

### Competitive Benchmarking
- Top-ranking videos in the same niche
- Average performance metrics
- Tag and keyword comparison

## 🎯 Recommendations Provided

The tool provides detailed recommendations across multiple areas:

### 1. **Title Optimization**
- Optimal length analysis (50-60 characters)
- Power words usage
- Number inclusion for higher CTR
- Comparison with top-performing titles

### 2. **Description Optimization**
- Length recommendations (200+ characters)
- Keyword placement
- Timestamp suggestions
- Link inclusion

### 3. **Tags Optimization**
- Optimal tag count (5-8 tags)
- Relevant tag suggestions from top videos
- Tag relevance analysis

### 4. **Thumbnail Optimization**
- Best practices for CTR
- Design recommendations
- A/B testing suggestions

### 5. **Engagement Strategies**
- CTA improvements
- Community building tips
- Response strategies based on sentiment

### 6. **SEO Improvements**
- Watch time optimization
- Posting schedule recommendations
- Platform-specific tactics
- Hashtag usage

### 7. **AI-Powered Insights** (Optional)
- Personalized recommendations
- Context-aware suggestions
- Priority-ranked action items

## ⚡ Intelligent Caching

The analyzer includes a smart caching system that significantly improves performance and reduces API quota usage:

### Benefits
- **Reduced API Usage**: Cached responses don't count against your YouTube API quota
- **Faster Analysis**: Re-analyzing videos is nearly instantaneous with cached data
- **Offline Development**: Test and develop without consuming API quota
- **Configurable TTL**: Set different cache lifetimes for different data types

### How It Works
- Video metadata cached for 1 hour (configurable)
- Comments cached for 30 minutes (configurable)
- Search results cached for 2 hours (configurable)
- Automatic cleanup of expired entries
- Cache stored locally in `.cache` directory

### Configuration
Edit `config.json` to customize cache settings:
```json
{
  "cache_settings": {
    "enabled": true,
    "cache_directory": ".cache",
    "default_ttl_seconds": 3600,
    "video_metadata_ttl_seconds": 3600,
    "comments_ttl_seconds": 1800,
    "search_results_ttl_seconds": 7200
  }
}
```

### Cache Management
```bash
# View cache statistics
python youseo.py --cache-stats

# Clear all cached data
python youseo.py --cache-clear

# Disable cache for one-time analysis
python youseo.py VIDEO_URL --no-cache
```

## 📄 Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           🎥  YouTube SEO Analyzer & Optimizer  🎥            ║
║                                                               ║
║         AI-Powered Video Analysis & Recommendations          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🔍 Analyzing video: https://www.youtube.com/watch?v=...
----------------------------------------------------------------------
Analyzing video: dQw4w9WgXcQ
✓ Fetched metadata for: Example Video Title
✓ Calculated engagement metrics
✓ Fetched 87 comments
✓ Found 5 top-ranking videos in niche

======================================================================
📹 VIDEO INFORMATION
======================================================================
Title: Example Video Title
Channel: Example Channel
Published: 2024-01-15
Views: 125,430
Engagement Rate: 4.2%

[... detailed analysis and recommendations ...]
```

## 🔧 Project Structure

```
youseo/
├── youseo.py                 # Main CLI application
├── youtube_analyzer.py       # YouTube API integration
├── sentiment_analyzer.py     # Comment sentiment analysis
├── recommendation_engine.py  # AI recommendation generator
├── batch_analyzer.py         # Batch video analysis
├── cache_manager.py          # Intelligent caching system
├── test_analyzer.py          # Core functionality tests
├── test_batch.py             # Batch analysis tests
├── test_cache.py             # Cache system tests
├── config.json               # Configuration settings
├── requirements.txt          # Python dependencies
├── example_videos.txt        # Example batch input file
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Important Notes

- **API Quotas**: YouTube Data API has daily quota limits. Use caching to minimize API usage!
- **Caching**: The tool automatically caches API responses to reduce quota consumption.
- **Rate Limiting**: The tool respects API rate limits to avoid issues.
- **Privacy**: Comments are analyzed locally and not stored permanently.
- **OpenAI Costs**: AI insights use OpenAI API which may incur costs based on usage.

## 🐛 Troubleshooting

### "YouTube API key is required"
- Ensure your `.env` file exists and contains a valid `YOUTUBE_API_KEY`

### "Video not found"
- Check that the video URL is correct and the video is public
- Ensure the video hasn't been deleted or made private

### "Comments disabled or error"
- Some videos have comments disabled - this is normal
- The tool will continue analysis without sentiment data

### "AI insights unavailable"
- Check your `OPENAI_API_KEY` in `.env`
- Use `--no-ai` flag to skip AI insights if key is not available

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions

## 🎓 Learn More

- [YouTube Creator Academy](https://creatoracademy.youtube.com/)
- [YouTube SEO Best Practices](https://support.google.com/youtube/answer/7631563)
- [YouTube Algorithm Explained](https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/)

---

Made with ❤️ for YouTube creators who want to grow their channels