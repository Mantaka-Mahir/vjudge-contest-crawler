# VJudge Contest Ranking Crawler

A Python application to extract ranking data from VJudge contest pages and save it to CSV files. Supports both GUI and command-line interfaces.

## Features

- Extract complete ranking data from VJudge contests
- Support for multiple contests in batch
- Export data to CSV format with proper formatting
- GUI interface for easy use
- Command-line interface for automation
- Detailed logging and progress tracking
- Configurable output directory
- Option to run in headless mode (without visible browser)

## Data Extracted

For each team in a contest, the following data is extracted:
- **Rank**: Team's position in the contest
- **Team Name**: Full team name with member names
- **Score**: Total number of problems solved
- **Penalty**: Total penalty time
- **Solved Problems**: Count of successfully solved problems
- **Individual Problem Results**: Submission time and attempts for each problem

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required packages:
   ```bash
   pip install requests beautifulsoup4 selenium pandas webdriver-manager
   ```
3. Download the source files to a directory

## Usage

### GUI Interface (Recommended)

1. Run the GUI application:
   ```bash
   python vjudge_gui.py
   ```

2. Use the interface to:
   - Add contest IDs (one at a time or multiple)
   - Select output directory
   - Choose headless mode option
   - Start crawling and monitor progress

### Command Line Interface

1. Basic usage:
   ```bash
   python crawl_cli.py CONTEST_ID
   ```

2. Multiple contests:
   ```bash
   python crawl_cli.py 739901 739902 739903
   ```

3. With options:
   ```bash
   python crawl_cli.py 739901 --output my_output --headless
   ```

### Programmatic Usage

```python
from vjudge_crawler import VJudgeRankingCrawler

# Create crawler instance
with VJudgeRankingCrawler(headless=True) as crawler:
    # Crawl single contest
    contest_data = crawler.get_contest_data("739901")
    
    # Save to CSV
    if contest_data:
        csv_file = crawler.save_to_csv(contest_data, "output")
        print(f"Data saved to: {csv_file}")
    
    # Or crawl multiple contests
    contest_ids = ["739901", "739902"]
    saved_files = crawler.crawl_multiple_contests(contest_ids, "output")
```

## Output Format

The CSV files contain the following columns:
- `Rank`: Team rank (1, 2, 3, ...)
- `Team Name`: Full team name
- `Score`: Number of problems solved
- `Penalty`: Total penalty time
- `Solved Problems`: Count of solved problems
- `Problem A`, `Problem B`, etc.: Individual problem results

Example CSV content:
```csv
Rank,Team Name,Score,Penalty,Solved Problems,A63 / 107,B60 / 196,...
1,"open your brain (Zhi Zhang, Yanru Guan, Jianfeng Zhu)",10,1240,10,0:55:00,1:27:00,...
2,"Screenwalkers (Hirotaka Yoneda, Masataka Yoneda, Daiki Kodama)",10,1580,10,0:56:00,1:46:00 (-2),...
```

## Requirements

- Python 3.7+
- Chrome or Chromium browser
- Internet connection
- Required Python packages (see Installation)

## Troubleshooting

### Common Issues

1. **Chrome driver issues**
   - The application automatically downloads the appropriate Chrome driver
   - If issues persist, try updating Chrome browser

2. **Contest not found**
   - Verify the contest ID is correct
   - Ensure the contest page is accessible
   - Some contests may be private or restricted

3. **Slow loading**
   - VJudge pages can be slow to load
   - The application waits for content to load automatically
   - Try running in headless mode for better performance

4. **Empty data**
   - Contest may not have started or ranking data may not be available
   - Try accessing the contest page manually to verify data exists

### Performance Tips

- Use headless mode (`--headless` in CLI or checkbox in GUI) for faster crawling
- Avoid crawling too many contests simultaneously
- Ensure stable internet connection

## File Structure

```
vjudge_crawler/
├── vjudge_crawler.py    # Main crawler class
├── vjudge_gui.py        # GUI application
├── crawl_cli.py         # Command-line interface
├── README.md            # This file
└── output/              # Default output directory (created automatically)
    ├── contest_739901_rankings.csv
    ├── contest_739902_rankings.csv
    └── ...
```

## Examples

### Example 1: GUI Usage
1. Run `python vjudge_gui.py`
2. Enter contest ID "739901"
3. Click "Add"
4. Click "Start Crawling"
5. Wait for completion and check the output folder

### Example 2: Batch Processing
```bash
python crawl_cli.py 739901 739902 739903 --output batch_results --headless
```

### Example 3: Programmatic Integration
```python
from vjudge_crawler import VJudgeRankingCrawler

def analyze_contest_performance(contest_id):
    with VJudgeRankingCrawler(headless=True) as crawler:
        data = crawler.get_contest_data(contest_id)
        
        if data:
            teams = data['teams']
            print(f"Contest {contest_id} Statistics:")
            print(f"- Total teams: {len(teams)}")
            print(f"- Average score: {sum(int(t['score']) for t in teams) / len(teams):.1f}")
            print(f"- Winner: {teams[0]['team']}")
            
            return data
        return None

# Analyze multiple contests
for contest_id in ["739901", "739902"]:
    analyze_contest_performance(contest_id)
```

## License

This project is provided as-is for educational and research purposes. Please respect VJudge's terms of service and use responsibly.

## Contributing

Feel free to submit issues, feature requests, or improvements. Make sure to test thoroughly before submitting changes.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all requirements are installed correctly
3. Test with a known working contest ID (e.g., 739901)
4. Check the log output for detailed error messages
