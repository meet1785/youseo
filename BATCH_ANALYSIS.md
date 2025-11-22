# Batch Analysis Feature

## Overview

The Batch Analysis feature allows you to analyze multiple YouTube videos in a single run, providing comparative insights and summary statistics across your content. This is especially useful for content creators who want to:

- Analyze their entire channel or multiple videos at once
- Compare performance across different videos
- Identify best and worst performing content
- Track improvements over time
- Make data-driven content decisions

## Key Benefits

1. **Time Efficiency**: Analyze dozens of videos in one command instead of running individual analyses
2. **Comparative Insights**: See which videos perform best and identify patterns
3. **API Quota Friendly**: Leverages the caching system to minimize YouTube API usage
4. **Flexible Input**: Support for file-based input (TXT/CSV) or direct URL listing
5. **Multiple Export Formats**: Export results as JSON for detailed analysis or CSV for spreadsheet tools

## Usage

### Method 1: File-Based Input (Recommended)

Create a text file with one video URL per line:

**videos.txt:**
```
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/shorts/SHORT_ID_1
# Lines starting with # are comments
https://www.youtube.com/watch?v=VIDEO_ID_3
```

Then run:
```bash
python youseo.py --batch videos.txt
```

### Method 2: CSV Input

Create a CSV file with URLs in the first column:

**videos.csv:**
```csv
URL,Title,Notes
https://www.youtube.com/watch?v=VIDEO_ID_1,My First Video,Tutorial
https://www.youtube.com/watch?v=VIDEO_ID_2,My Second Video,Review
https://www.youtube.com/shorts/SHORT_ID_1,My Short,Short-form
```

Then run:
```bash
python youseo.py --batch videos.csv --batch-format csv
```

### Method 3: Command Line URLs

For a small number of videos, you can provide URLs directly:

```bash
python youseo.py --urls \
  https://www.youtube.com/watch?v=VIDEO_ID_1 \
  https://www.youtube.com/watch?v=VIDEO_ID_2 \
  https://www.youtube.com/shorts/SHORT_ID_1
```

## Command Line Options

### Batch Analysis Options

- `--batch FILE`: Analyze videos from a file (TXT or CSV format)
- `--urls URL [URL ...]`: Analyze multiple URLs provided directly
- `--batch-output FILE`: Specify output file (default: batch_results.json)
- `--batch-format {json,csv}`: Choose output format (default: json)

### Combined with Other Options

All standard options work with batch analysis:

```bash
# Batch analysis without AI insights
python youseo.py --batch videos.txt --no-ai

# Batch analysis without comment analysis (faster)
python youseo.py --batch videos.txt --no-comments

# Batch analysis with limited comments per video
python youseo.py --batch videos.txt --max-comments 50

# Batch analysis without cache
python youseo.py --batch videos.txt --no-cache
```

## Output Formats

### JSON Output (Default)

The JSON output includes:
- Summary statistics (total views, average engagement, etc.)
- Best/worst performing videos
- Complete analysis data for each video
- Recommendations for each video

**Example structure:**
```json
{
  "summary": {
    "total_videos": 5,
    "total_views": 50000,
    "average_views": 10000,
    "average_engagement_rate": 4.5,
    "best_performing": {
      "title": "Best Video Title",
      "views": 25000,
      "url": "..."
    },
    "worst_performing": {...},
    "highest_engagement": {...},
    "lowest_engagement": {...}
  },
  "videos": [
    {
      "url": "...",
      "video_id": "...",
      "analysis_data": {...},
      "recommendations": {...}
    }
  ]
}
```

### CSV Output

The CSV output provides a spreadsheet-friendly format with key metrics:

| title | url | views | likes | comments | engagement_rate | like_rate | overall_sentiment | title_score | description_score | tags_score |
|-------|-----|-------|-------|----------|----------------|-----------|-------------------|-------------|-------------------|------------|
| Video 1 | ... | 10000 | 500 | 50 | 5.5 | 5.0 | positive | 85 | 75 | 70 |
| Video 2 | ... | 8000 | 400 | 40 | 5.5 | 5.0 | positive | 90 | 80 | 75 |

Perfect for:
- Importing into Excel, Google Sheets, or other spreadsheet tools
- Creating charts and visualizations
- Quick overview of video performance

## Summary Report

After batch analysis, you'll see a summary report in the terminal:

```
======================================================================
📊 BATCH ANALYSIS SUMMARY
======================================================================

Total Videos Analyzed: 5
Total Views: 50,000
Average Views per Video: 10,000
Average Engagement Rate: 4.50%
Average Like Rate: 4.20%

🏆 Best Performing Video (by views):
  Title: Amazing Tutorial: Complete Guide 2024
  Views: 25,000
  URL: https://www.youtube.com/watch?v=...

📉 Needs Improvement (lowest views):
  Title: Quick Tip #3
  Views: 3,500
  URL: https://www.youtube.com/watch?v=...

💬 Highest Engagement:
  Title: Q&A Session with Community
  Engagement Rate: 8.50%
  URL: https://www.youtube.com/watch?v=...

😴 Lowest Engagement:
  Title: Product Announcement
  Engagement Rate: 2.10%
  URL: https://www.youtube.com/watch?v=...
```

## Use Cases

### 1. Channel Performance Audit

Analyze all videos on your channel to identify:
- Which video types perform best
- Optimal video length for your audience
- Best performing topics
- Title/thumbnail patterns that work

```bash
# Create a file with all your video URLs
python youseo.py --batch my_channel_videos.txt --batch-output channel_audit.json
```

### 2. Series Comparison

Compare videos in a series to see which episodes perform best:

```bash
python youseo.py --batch tutorial_series.txt --batch-format csv
```

### 3. Content Strategy Testing

Compare different content types:

```bash
# Analyze tutorials vs reviews vs shorts
python youseo.py --batch content_experiments.txt
```

### 4. Competitor Analysis

Analyze top videos from competitors to identify winning patterns:

```bash
python youseo.py --batch competitor_top_videos.txt --no-comments
```

### 5. Historical Performance Tracking

Re-run batch analysis weekly/monthly to track improvements:

```bash
python youseo.py --batch monitored_videos.txt --batch-output "weekly_report_$(date +%Y%m%d).json"
```

## Best Practices

### 1. Use Caching for Repeated Analysis

The caching system is especially valuable for batch analysis:
- First run: Full API calls, takes longer
- Subsequent runs: Much faster, minimal API usage
- Clear cache when you want fresh data

```bash
# Clear cache before fresh analysis
python youseo.py --cache-clear
python youseo.py --batch videos.txt
```

### 2. Start Small

Test with a few videos first before analyzing your entire channel:

```bash
# Test with 5 videos
python youseo.py --urls URL1 URL2 URL3 URL4 URL5
```

### 3. Skip Comments for Large Batches

If analyzing many videos, skip comment analysis to save time and API quota:

```bash
python youseo.py --batch large_list.txt --no-comments
```

### 4. Use Appropriate Export Format

- Use JSON for complete data and further processing
- Use CSV for quick overview and spreadsheet analysis

### 5. Monitor API Quota

- Free YouTube API tier: 10,000 units/day
- Each video analysis: ~100-200 units (without cache)
- With cache: 0 units for cached videos
- Plan accordingly for large batches

## Error Handling

The batch analyzer is resilient:
- **Invalid URLs**: Skipped with warning, analysis continues
- **Private/Deleted Videos**: Skipped with error message
- **API Errors**: Individual video errors don't stop batch processing
- **File Errors**: Clear error messages for file issues

## Performance Considerations

### Analysis Speed

- Without cache: ~3-5 seconds per video
- With cache: <1 second per video
- 10 videos without cache: ~30-50 seconds
- 10 videos with cache: ~10-15 seconds

### API Quota Usage

- Single video (uncached): ~100-200 quota units
- 50 videos (uncached): ~5,000-10,000 units (full daily quota)
- 50 videos (cached): 0 additional units

**Recommendation**: Use cache for regular batch analyses of the same videos.

## Troubleshooting

### "No URLs found to analyze"
- Check that your file exists and contains valid URLs
- Ensure URLs are on separate lines (TXT) or in first column (CSV)

### "File not found"
- Verify the file path is correct
- Use absolute path if relative path doesn't work

### Slow analysis
- First run is always slower (no cache)
- Use `--no-comments` for faster analysis
- Check internet connection

### API quota exceeded
- Check quota usage in Google Cloud Console
- Use `--cache-stats` to see cache effectiveness
- Wait for quota to reset (daily)

## Examples

### Complete workflow example:

```bash
# 1. Create input file
cat > my_videos.txt << EOF
https://www.youtube.com/watch?v=VIDEO_1
https://www.youtube.com/watch?v=VIDEO_2
https://www.youtube.com/shorts/SHORT_1
EOF

# 2. Run batch analysis
python youseo.py --batch my_videos.txt --batch-output analysis.json

# 3. Also export as CSV for spreadsheet
python youseo.py --batch my_videos.txt --batch-format csv --batch-output analysis.csv

# 4. Check cache statistics
python youseo.py --cache-stats
```

## Integration with Existing Features

Batch analysis works seamlessly with all existing features:
- ✅ Sentiment analysis (optional with `--no-comments`)
- ✅ AI insights (optional with `--no-ai`)
- ✅ Caching system (use `--no-cache` to disable)
- ✅ Custom comment limits (use `--max-comments`)
- ✅ Regular videos and Shorts

---

For more information, see:
- [README.md](README.md) - Main documentation
- [USAGE.md](USAGE.md) - Detailed usage guide
- [CACHING_FEATURE.md](CACHING_FEATURE.md) - Caching system details
