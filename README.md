# VJudge Contest Ranking Crawler

An independent HTTP-based Python scraper to extract ranking data from VJudge contest pages and save it to CSV files. Features command-line interface for automation and batch processing.

## Features

- ✅ **Independent Operation** - No manual browser required
- ✅ **HTTP-First Approach** - Fast extraction using direct API calls
- ✅ **Smart Fallback** - Automatic browser automation when needed
- ✅ **Batch Processing** - Handle multiple contests in one command
- ✅ **Clean CSV Output** - Structured data in standard format
- ✅ **Command-line Interface** - Perfect for automation and scripting
- ✅ **Timestamped Files** - No file conflicts

## Data Extracted

For each participant in a contest, the following data is extracted and saved in CSV format:
- **Rank**: Participant's position in the contest (1, 2, 3, ...)
- **Team**: Full team name with member handles
- **Score**: Total number of problems solved
- **Penalty**: Total penalty time in minutes
- **Solved**: Number of successfully solved problems

## CSV Output Format

The scraper generates clean CSV files with the following structure:
```csv
rank,team,score,penalty,solved
1,Krutoichel (Timoxa zhir),6,279,6
2,zxzuam (Aza),6,1076,6
3,ARSENTOP1LEGENDA (Ars),5,429,5
4,Mukhamediyar2011 (Mukha),5,577,5
5,zertinii (Isma),5,661,5
6,Sarsenbai_008,3,269,3
```

## Installation

### Method 1: From GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/Mantaka-Mahir/vjudge-contest-crawler.git
cd vjudge-contest-crawler

# Set up virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Manual Installation
1. Make sure you have Python 3.7+ installed
2. Install required packages:
   ```bash
   pip install requests beautifulsoup4 selenium pandas webdriver-manager
   ```
3. Download the source files to a directory

## Usage

### Command Line Interface

The main tool is `crawl_cli.py` which provides a simple command-line interface for extracting contest data.

#### Basic Syntax
```bash
python crawl_cli.py [contest_id] [contest_id] ... [options]
```

#### Examples

**Single Contest:**
```bash
python crawl_cli.py 740062
```

**Multiple Contests:**
```bash
python crawl_cli.py 740062 739901 741234
```

**Custom Output Directory:**
```bash
python crawl_cli.py 740062 -o custom_output
```

**Verbose Output:**
```bash
python crawl_cli.py 740062 -v
```

**Multiple Contests with Custom Output:**
```bash
python crawl_cli.py 740062 739901 741234 -o contest_results -v
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `contest_ids` | One or more VJudge contest IDs (required) | - |
| `-o, --output` | Output directory for CSV files | `output` |
| `-v, --verbose` | Enable detailed output and error messages | `False` |
| `--version` | Show version information | - |

### Programmatic Usage

```python
from vjudge_crawler import VJudgeRankingCrawler

# Create crawler instance
crawler = VJudgeRankingCrawler(output_dir="output")

# Crawl single contest and save to CSV
csv_file = crawler.crawl_contest("740062")
if csv_file:
    print(f"Data saved to: {csv_file}")

# Process multiple contests
contest_ids = ["740062", "739901"]
for contest_id in contest_ids:
    print(f"Processing contest {contest_id}...")
    csv_file = crawler.crawl_contest(contest_id)
    if csv_file:
        print(f"✓ Success: {csv_file}")
    else:
        print(f"✗ Failed: {contest_id}")

# Close crawler
crawler.close()
```

## How It Works

### 1. HTTP-First Approach
The scraper first attempts to extract data using direct HTTP requests to VJudge endpoints:
- Faster execution
- Lower resource usage  
- No browser dependencies

### 2. Browser Automation Fallback
If HTTP extraction fails (e.g., for dynamic content), the tool automatically:
- Launches Chrome in headless mode
- Loads the contest page
- Extracts ranking data via JavaScript
- Closes the browser session

### 3. Smart Table Detection
The scraper intelligently identifies ranking tables by:
- Looking for participant names and time patterns
- Analyzing table structure and content
- Scoring tables based on ranking data characteristics

## Output Format

The CSV files contain the following columns in this exact order:
- `rank` - Contest ranking position (1, 2, 3, ...)
- `team` - Team/participant name with handle
- `score` - Total number of problems solved  
- `penalty` - Total penalty time in minutes
- `solved` - Number of successfully solved problems

### File Naming
Output files are automatically named with timestamps to prevent conflicts:
```
vjudge_contest_{contest_id}_rankings_{YYYYMMDD_HHMMSS}.csv
```

Example: `vjudge_contest_740062_rankings_20250816_182618.csv`

## Requirements

- Python 3.7+
- Internet connection
- Chrome browser (automatically managed for fallback)
- Required Python packages:
  - `requests` - HTTP requests
  - `beautifulsoup4` - HTML parsing  
  - `selenium` - Browser automation (fallback)
  - `pandas` - Data processing
  - `webdriver-manager` - Chrome driver management

## Troubleshooting

### Common Issues

**Contest Not Found (404 Error):**
```
Endpoint returned status 404
```
- Verify the contest ID is correct
- Check if the contest is public/accessible
- Some contests may be private or deleted

**No Ranking Data:**
```
No ranking table found with participant data
```
- Contest might be empty (no participants)
- Contest might not have started yet
- Try running with `-v` for detailed analysis

**Permission Errors:**
```
Error saving CSV: Permission denied
```
- Ensure output directory is writable
- Close any Excel/CSV applications using the output files
- Try a different output directory with `-o`

### Verbose Mode

Use `-v` flag for detailed debugging information:
```bash
python crawl_cli.py 740062 -v
```

This will show:
- HTTP endpoint attempts
- Table analysis details
- Browser automation steps (if needed)
- Detailed error messages

### Performance Tips

- Use batch processing for multiple contests: `python crawl_cli.py 740062 739901 741234`
- Ensure stable internet connection for reliable extraction
- Large contests may take longer to process
- Regularly clean old CSV files from output directory

## File Structure

```
vjudge-contest-crawler/
├── .gitignore              # Git ignore file
├── INSTRUCTIONS.md         # Complete usage guide
├── PROJECT_SUMMARY.md      # Technical summary
├── README.md              # This file
├── crawl_cli.py           # Command-line interface
├── requirements.txt       # Python dependencies
├── setup.py              # Installation script
├── vjudge_crawler.py      # Main crawler engine
└── output/                # Default output directory (created automatically)
    ├── vjudge_contest_740062_rankings_20250816_182618.csv
    ├── vjudge_contest_739901_rankings_20250816_182619.csv
    └── ...
```

## Examples

### Example 1: Single Contest Extraction
```bash
python crawl_cli.py 740062
```

**Expected Output:**
```
VJudge Contest Ranking Crawler (HTTP Mode)
==================================================
Contest IDs: 740062
Output directory: output
Mode: HTTP requests (no browser required)
==================================================

[1/1] Processing contest 740062...
✓ Success: vjudge_contest_740062_rankings_20250816_182618.csv

==================================================
CRAWLING SUMMARY
==================================================
Total contests processed: 1
Successful: 1
Failed: 0

Saved files:
  • .\output\vjudge_contest_740062_rankings_20250816_182618.csv
```

### Example 2: Batch Processing
```bash
python crawl_cli.py 740062 739901 741234 -o batch_results -v
```

### Example 3: Programmatic Integration
```python
from vjudge_crawler import VJudgeRankingCrawler

def analyze_contest_performance(contest_id):
    crawler = VJudgeRankingCrawler()
    csv_file = crawler.crawl_contest(contest_id)
    
    if csv_file:
        import pandas as pd
        df = pd.read_csv(csv_file)
        
        print(f"Contest {contest_id} Statistics:")
        print(f"- Total participants: {len(df)}")
        print(f"- Average score: {df['score'].mean():.1f}")
        print(f"- Winner: {df.iloc[0]['team']}")
        
        return csv_file
    
    crawler.close()
    return None

# Analyze multiple contests
for contest_id in ["740062", "739901"]:
    analyze_contest_performance(contest_id)
```

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run with `-v` flag for detailed output
3. Verify contest IDs and accessibility
4. Ensure all dependencies are installed correctly
5. Check the [INSTRUCTIONS.md](INSTRUCTIONS.md) for comprehensive usage guide

## Version Information
- **Version**: 2.0 (HTTP Mode)
- **Python**: 3.7+ required
- **Dependencies**: See `requirements.txt`
- **Platform**: Windows, Linux, macOS

## License

This project is provided as-is for educational and research purposes. Please respect VJudge's terms of service and use responsibly.

## Contributing

Feel free to submit issues, feature requests, or improvements via GitHub. Make sure to test thoroughly before submitting changes.

---

**Repository**: https://github.com/Mantaka-Mahir/vjudge-contest-crawler

**Note**: This tool respects VJudge's terms of service and implements reasonable delays to avoid overwhelming their servers.
