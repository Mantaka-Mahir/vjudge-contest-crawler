# VJudge Contest Ranking Crawler - Instructions

## Overview
This is an independent HTTP-based scraper that extracts contest ranking data from VJudge without requiring manual browser interaction. The tool uses HTTP requests as the primary method with intelligent browser automation fallback for dynamic content.

## Features
- ✅ **Independent Operation** - No manual browser required
- ✅ **HTTP-First Approach** - Fast extraction using direct API calls
- ✅ **Smart Fallback** - Automatic browser automation when needed
- ✅ **Batch Processing** - Handle multiple contests in one command
- ✅ **Clean CSV Output** - Structured data in standard format
- ✅ **Timestamped Files** - No file conflicts

## Installation

### 1. Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd vjudge_crawler

# Or download and extract the ZIP file
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate

# On Linux/Mac:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

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

### Output Format

The scraper generates CSV files with the following structure:

```csv
rank,team,score,penalty,solved
1,Krutoichel (Timoxa zhir),6,279,6
2,zxzuam (Aza),6,1076,6
3,ARSENTOP1LEGENDA (Ars),5,429,5
4,Mukhamediyar2011 (Mukha),5,577,5
5,zertinii (Isma),5,661,5
6,Sarsenbai_008,3,269,3
```

**Column Descriptions:**
- `rank` - Contest ranking position
- `team` - Team/participant name with handle
- `score` - Total problems solved
- `penalty` - Time penalty in minutes
- `solved` - Number of problems solved

### File Naming

Output files are automatically named with timestamps to prevent conflicts:
```
vjudge_contest_{contest_id}_rankings_{YYYYMMDD_HHMMSS}.csv
```

Example: `vjudge_contest_740062_rankings_20250816_182618.csv`

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
- Browser automation steps
- Detailed error messages

## Performance Tips

1. **Batch Processing**: Process multiple contests in one command for efficiency
2. **Network**: Ensure stable internet connection for reliable extraction
3. **Resources**: Large contests may take longer to process
4. **Output**: Regularly clean old CSV files from output directory

## Examples with Expected Results

### Single Contest Extraction
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

### Multiple Contest Extraction
```bash
python crawl_cli.py 740062 739901 741234 -o results
```

**Expected Output:**
```
VJudge Contest Ranking Crawler (HTTP Mode)
==================================================
Contest IDs: 740062, 739901, 741234
Output directory: results
Mode: HTTP requests (no browser required)
==================================================

[1/3] Processing contest 740062...
✓ Success: vjudge_contest_740062_rankings_20250816_182618.csv

[2/3] Processing contest 739901...
✓ Success: vjudge_contest_739901_rankings_20250816_182619.csv

[3/3] Processing contest 741234...
✗ Failed: Unable to extract data for contest 741234

==================================================
CRAWLING SUMMARY
==================================================
Total contests processed: 3
Successful: 2
Failed: 1

Saved files:
  • results\vjudge_contest_740062_rankings_20250816_182618.csv
  • results\vjudge_contest_739901_rankings_20250816_182619.csv

Failed contests: 741234
```

## Advanced Usage

### Processing Contest Lists from File
```bash
# Create a file with contest IDs (one per line)
echo 740062 > contests.txt
echo 739901 >> contests.txt
echo 741234 >> contests.txt

# Process all contests
python crawl_cli.py $(Get-Content contests.txt) -o batch_results
```

### Automated Data Collection
```bash
# Create a batch script for regular collection
@echo off
cd /d "C:\path\to\vjudge_crawler"
.\.venv\Scripts\python.exe crawl_cli.py 740062 739901 -o daily_results -v
echo Extraction completed at %date% %time%
```

## Support

For issues or questions:
1. Check this documentation
2. Run with `-v` flag for detailed output
3. Verify contest IDs and accessibility
4. Ensure all dependencies are installed correctly

## Version Information
- **Version**: 2.0 (HTTP Mode)
- **Python**: 3.7+ required
- **Dependencies**: See `requirements.txt`
- **Platform**: Windows, Linux, macOS

---

**Note**: This tool respects VJudge's terms of service and implements reasonable delays to avoid overwhelming their servers.
