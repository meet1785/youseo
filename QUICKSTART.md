# Quick Start Guide

Get started with YouTube SEO Analyzer in 5 minutes!

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/meet1785/youseo.git
cd youseo

# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually install
pip install -r requirements.txt
```

## 🔑 API Keys Setup

### Required: YouTube Data API v3

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable "YouTube Data API v3"
4. Create API Key
5. Copy to `.env`:

```bash
cp .env.example .env
# Edit .env and add:
YOUTUBE_API_KEY=your_key_here
```

### Optional: OpenAI API

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Generate API key
3. Add to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

## 📺 Try It Out

### Demo Mode (No API Keys Required)
```bash
python demo.py
```

### Test Suite
```bash
python test_analyzer.py
```

### Analyze Your First Video
```bash
python youseo.py https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

## 📖 Common Commands

```bash
# Basic analysis
python youseo.py https://www.youtube.com/watch?v=VIDEO_ID

# Save report to file
python youseo.py VIDEO_URL --output report.json

# Skip AI insights (faster, no OpenAI key needed)
python youseo.py VIDEO_URL --no-ai

# Skip comments (faster)
python youseo.py VIDEO_URL --no-comments

# Analyze a Short
python youseo.py https://www.youtube.com/shorts/VIDEO_ID

# Get help
python youseo.py --help
```

## 📊 Understanding Your Results

The analyzer provides scores (0-100) and suggestions for:

- **Title** - Optimal length, keywords, power words
- **Description** - Length, keyword placement, links
- **Tags** - Quantity and relevance
- **Thumbnail** - Design best practices
- **Engagement** - Like/comment rates
- **SEO** - Overall optimization tips

### Score Interpretation
- **90-100**: Excellent - minor tweaks only
- **70-89**: Good - some improvements recommended
- **50-69**: Fair - several areas need attention
- **Below 50**: Needs work - prioritize improvements

## 🎯 Quick Wins

After your first analysis, focus on these for immediate impact:

1. **Title optimization** (highest CTR impact)
2. **Thumbnail** (works with title for clicks)
3. **First 30 seconds** (retention)
4. **Tags** (discoverability)
5. **Description** (SEO)

## 📚 Learn More

- Full documentation: [USAGE.md](USAGE.md)
- Code examples: [examples.py](examples.py)
- Detailed README: [README.md](README.md)

## 🆘 Need Help?

**"YouTube API key is required"**
- Check `.env` file exists and has valid `YOUTUBE_API_KEY`

**"Video not found"**
- Ensure video is public
- Check URL format

**"Comments disabled"**
- Normal! Use `--no-comments` flag

**Other issues?**
- Check [USAGE.md](USAGE.md) troubleshooting section
- Open an issue on GitHub

## 💡 Pro Tips

- Analyze competitor videos first
- Compare with your best-performing videos
- Re-analyze after implementing changes
- Track improvements over time
- Focus on one change at a time

---

**Ready to optimize your videos? Start with the demo!**

```bash
python demo.py
```
