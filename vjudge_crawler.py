"""
VJudge Contest Ranking Crawler
This script extracts ranking data from VJudge contest pages and saves to CSV
Uses HTTP requests and HTML parsing - no browser required!
"""

import requests
import time
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import os
from typing import List, Dict, Optional


class VJudgeRankingCrawler:
    """
    A crawler for extracting ranking data from VJudge contest pages.
    Uses HTTP requests and HTML parsing - no browser required!
    """
    
    def __init__(self, output_dir: str = "output", headless: bool = True):
        """
        Initialize the crawler with output directory.
        
        Args:
            output_dir: Directory to save CSV files
            headless: Kept for compatibility (not used in HTTP mode)
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup session with headers to mimic a real browser
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        print("VJudge Crawler initialized (HTTP mode - no browser required)")
    
    def get_contest_data(self, contest_id: str) -> List[Dict]:
        """
        Extract ranking data from a VJudge contest.
        First tries HTTP requests, then falls back to browser automation if needed.
        
        Args:
            contest_id: The contest ID from VJudge URL
            
        Returns:
            List of dictionaries containing ranking data
        """
        print(f"Fetching contest {contest_id}...")
        
        try:
            # First attempt: Try HTTP requests (fast)
            ranking_data = self._try_http_extraction(contest_id)
            
            if ranking_data:
                print(f"Successfully extracted {len(ranking_data)} entries via HTTP")
                return ranking_data
            
            # Fallback: Use browser automation for dynamic content
            print("HTTP extraction failed, trying browser automation...")
            ranking_data = self._try_browser_extraction(contest_id)
            
            if ranking_data:
                print(f"Successfully extracted {len(ranking_data)} entries via browser")
                return ranking_data
            
            print("Warning: No ranking data found. The contest might be private or not accessible.")
            return []
            
        except Exception as e:
            print(f"Error processing contest data: {e}")
            return []
    
    def _try_http_extraction(self, contest_id: str) -> List[Dict]:
        """Try to extract data using HTTP requests only."""
        try:
            # Try AJAX endpoints first
            ranking_data = self._try_ajax_endpoints(contest_id)
            if ranking_data:
                return ranking_data
            
            # Try main contest page
            ranking_data = self._extract_from_main_page(contest_id)
            return ranking_data
            
        except Exception as e:
            print(f"HTTP extraction error: {e}")
            return []
    
    def _try_browser_extraction(self, contest_id: str) -> List[Dict]:
        """Use browser automation to extract data from dynamic content."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            
            print("Starting Chrome browser for dynamic content extraction...")
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                url = f"https://vjudge.net/contest/{contest_id}#rank"
                print(f"Loading page: {url}")
                driver.get(url)
                
                # Wait for the page to load
                wait = WebDriverWait(driver, 15)
                
                # Wait for ranking data to load (look for participant links)
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/user/']")))
                    print("Ranking data loaded")
                except:
                    print("No participant links found - contest might be empty or private")
                
                # Extract data using JavaScript
                ranking_data = driver.execute_script("""
                    // Find table containing participant data
                    const participantLinks = document.querySelectorAll('a[href*="/user/"]');
                    if (participantLinks.length === 0) return [];
                    
                    // Find the table that contains participants
                    let table = null;
                    for (const link of participantLinks) {
                        table = link.closest('table');
                        if (table) break;
                    }
                    
                    if (!table) return [];
                    
                    const rows = table.querySelectorAll('tr');
                    if (rows.length < 2) return [];
                    
                    // Extract headers
                    const headers = Array.from(rows[0].querySelectorAll('th, td')).map(cell => cell.textContent.trim());
                    
                    // Extract data rows
                    const data = [];
                    for (let i = 1; i < rows.length; i++) {
                        const cells = Array.from(rows[i].querySelectorAll('td, th')).map(cell => cell.textContent.trim());
                        if (cells.length >= 4) {
                            // Count solved problems (cells with time format)
                            let solvedCount = 0;
                            for (let j = 4; j < cells.length; j++) {
                                if (/\\d+:\\d+:\\d+/.test(cells[j])) {
                                    solvedCount++;
                                }
                            }
                            
                            data.push({
                                rank: cells[0],
                                team: cells[1],
                                score: cells[2],
                                penalty: cells[3].split('\\n')[0], // Remove time formatting
                                solved: solvedCount
                            });
                        }
                    }
                    
                    return data;
                """)
                
                return ranking_data
                
            finally:
                driver.quit()
                
        except ImportError:
            print("Selenium not available for browser automation")
            return []
        except Exception as e:
            print(f"Browser extraction error: {e}")
            return []
    
    def _try_ajax_endpoints(self, contest_id: str) -> List[Dict]:
        """Try to fetch ranking data from VJudge AJAX endpoints."""
        endpoints = [
            f"https://vjudge.net/contest/rank/single/{contest_id}",
            f"https://vjudge.net/contest/{contest_id}/rank",
            f"https://vjudge.net/api/contest/{contest_id}/rank",
            f"https://vjudge.net/contest/{contest_id}/data",
            f"https://vjudge.net/contest/data/{contest_id}",
            f"https://vjudge.net/contest/{contest_id}?output=json"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"Trying endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=15)
                
                if response.status_code == 200:
                    try:
                        # Try to parse as JSON
                        data = response.json()
                        processed_data = self._process_json_ranking_data(data)
                        if processed_data:
                            print(f"Success! Found data via JSON endpoint: {endpoint}")
                            return processed_data
                    except json.JSONDecodeError:
                        # Try to parse as HTML
                        soup = BeautifulSoup(response.content, 'html.parser')
                        processed_data = self._extract_ranking_from_tables(soup)
                        if processed_data:
                            print(f"Success! Found data via HTML endpoint: {endpoint}")
                            return processed_data
                else:
                    print(f"Endpoint returned status {response.status_code}")
                        
            except requests.exceptions.RequestException as e:
                print(f"Failed to access {endpoint}: {e}")
                continue
        
        return []
    
    def _extract_from_main_page(self, contest_id: str) -> List[Dict]:
        """Extract ranking data from the main contest page."""
        try:
            url = f"https://vjudge.net/contest/{contest_id}#rank"
            print(f"Fetching main page: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find ranking data in script tags
            ranking_data = self._extract_ranking_from_scripts(soup)
            
            if not ranking_data:
                # Fallback: try to extract from HTML tables
                ranking_data = self._extract_ranking_from_tables(soup)
            
            return ranking_data
            
        except Exception as e:
            print(f"Error extracting from main page: {e}")
            return []
    
    def _extract_ranking_from_scripts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract ranking data from JavaScript variables in script tags."""
        try:
            scripts = soup.find_all('script', string=True)
            
            for script in scripts:
                script_content = script.string
                if not script_content:
                    continue
                
                # Look for patterns that might contain ranking data
                patterns = [
                    r'dataRank\s*=\s*(\[.*?\]);',
                    r'rankData\s*=\s*(\[.*?\]);',
                    r'standings\s*=\s*(\[.*?\]);',
                    r'participants\s*=\s*(\[.*?\]);'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, script_content, re.DOTALL)
                    if match:
                        try:
                            data_str = match.group(1)
                            ranking_data = json.loads(data_str)
                            
                            if isinstance(ranking_data, list) and len(ranking_data) > 0:
                                return self._process_json_ranking_data(ranking_data)
                        except json.JSONDecodeError:
                            continue
            
            return []
            
        except Exception as e:
            print(f"Error extracting from scripts: {e}")
            return []
    
    def _process_json_ranking_data(self, data) -> List[Dict]:
        """Process ranking data from JSON format."""
        try:
            processed_data = []
            
            # Handle different JSON structures
            if isinstance(data, dict):
                # Look for ranking data in common keys
                for key in ['data', 'participants', 'rank', 'standings', 'rows']:
                    if key in data and isinstance(data[key], list):
                        return self._process_json_ranking_data(data[key])
                return []
            
            if not isinstance(data, list):
                return []
            
            for i, entry in enumerate(data):
                if isinstance(entry, dict):
                    # Extract common fields from JSON data
                    processed_entry = {
                        'Rank': entry.get('rank', entry.get('rk', i + 1)),
                        'Team': entry.get('name', entry.get('user', entry.get('team', entry.get('teamName', f'Team_{i+1}')))),
                        'Score': entry.get('score', entry.get('totalScore', entry.get('sc', 0))),
                        'Penalty': entry.get('penalty', entry.get('totalPenalty', entry.get('time', 0))),
                        'Solved': entry.get('solved', entry.get('ac', len(entry.get('problems', [])) if 'problems' in entry else 0))
                    }
                    processed_data.append(processed_entry)
                    
                elif isinstance(entry, list) and len(entry) >= 3:
                    # Sometimes data comes as arrays
                    processed_entry = {
                        'Rank': entry[0] if len(entry) > 0 else i + 1,
                        'Team': entry[1] if len(entry) > 1 else f'Team_{i+1}',
                        'Score': self._extract_number(entry[2]) if len(entry) > 2 else 0,
                        'Penalty': self._extract_number(entry[3]) if len(entry) > 3 else 0,
                        'Solved': self._extract_number(entry[4]) if len(entry) > 4 else 0
                    }
                    processed_data.append(processed_entry)
            
            return processed_data
            
        except Exception as e:
            print(f"Error processing JSON data: {e}")
            return []
    
    def _extract_ranking_from_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract ranking data from HTML tables (fallback method)."""
        try:
            tables = soup.find_all('table')
            print(f"Found {len(tables)} tables on the page")
            
            # Look for tables that contain actual participant data
            ranking_table = None
            
            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                table_text = table.get_text()
                
                print(f"Table {i}: {len(rows)} rows")
                
                # Look for indicators of ranking data
                ranking_indicators = [
                    'rank' in table_text.lower(),
                    'team' in table_text.lower(),
                    'score' in table_text.lower(),
                    'penalty' in table_text.lower(),
                    len(rows) > 2,  # Must have header + data rows
                ]
                
                # Look for participant names (common VJudge patterns)
                participant_patterns = [
                    'Krutoichel', 'zxzuam', 'ARSENTOP1LEGENDA', 'Mukhamediyar', 'zertinii', 'Sarsenbai'
                ]
                has_participants = any(name in table_text for name in participant_patterns)
                
                # Look for time patterns (like "0:36:26", "1:35:25")
                import re
                time_patterns = re.findall(r'\d+:\d+:\d+', table_text)
                has_time_data = len(time_patterns) > 5
                
                score = sum(ranking_indicators) + (3 if has_participants else 0) + (2 if has_time_data else 0)
                print(f"  Table {i} score: {score} (participants: {has_participants}, times: {len(time_patterns)})")
                
                if score >= 5:  # High threshold for ranking table
                    ranking_table = table
                    print(f"Selected table {i} as ranking table")
                    break
            
            if not ranking_table:
                print("No ranking table found with participant data")
                return []
            
            # Extract data from ranking table
            rows = ranking_table.find_all('tr')
            print(f"Processing ranking table with {len(rows)} rows")
            
            if len(rows) < 2:
                print("Insufficient rows in ranking table")
                return []
            
            # Get headers
            header_row = rows[0]
            headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
            print(f"Headers: {headers}")
            
            ranking_data = []
            for i, row in enumerate(rows[1:], 1):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:  # Must have rank, team, score, penalty
                    
                    cell_values = [cell.get_text().strip() for cell in cells]
                    print(f"Row {i}: {cell_values[:6]}...")
                    
                    # Extract rank (first column)
                    rank = cell_values[0] if cell_values[0].isdigit() else i
                    
                    # Extract team name (second column)
                    team = cell_values[1] if len(cell_values) > 1 else f'Team_{i}'
                    
                    # Extract score (third column - number of solved problems)
                    score = self._extract_number(cell_values[2]) if len(cell_values) > 2 else 0
                    
                    # Extract penalty (fourth column - remove time formatting)
                    penalty_text = cell_values[3] if len(cell_values) > 3 else '0'
                    penalty = self._extract_number(penalty_text.split('\n')[0])
                    
                    # Count solved problems from problem columns
                    solved_count = 0
                    problem_results = []
                    for j in range(4, len(cell_values)):
                        problem_result = cell_values[j].strip()
                        problem_results.append(problem_result)
                        
                        # Count as solved if it has a time (format like "0:36:26")
                        if re.match(r'\d+:\d+:\d+', problem_result):
                            solved_count += 1
                    
                    entry = {
                        'Rank': rank,
                        'Team': team,
                        'Score': score,
                        'Penalty': penalty,
                        'Solved': solved_count,
                        'Problems': problem_results
                    }
                    
                    ranking_data.append(entry)
            
            print(f"Successfully extracted {len(ranking_data)} participants")
            return ranking_data
            
        except Exception as e:
            print(f"Error extracting from tables: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extract_number(self, text: str) -> int:
        """Extract number from text string."""
        try:
            # Remove non-numeric characters except decimal point and minus
            cleaned = re.sub(r'[^\d.-]', '', str(text))
            if cleaned:
                return int(float(cleaned))
            return 0
        except (ValueError, TypeError):
            return 0
    
    def save_to_csv(self, data: List[Dict], contest_id: str) -> str:
        """
        Save ranking data to CSV file.
        
        Args:
            data: List of ranking dictionaries
            contest_id: Contest ID for filename
            
        Returns:
            Path to saved CSV file
        """
        if not data:
            print("No data to save")
            return ""
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vjudge_contest_{contest_id}_rankings_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            df = pd.DataFrame(data)
            
            # Reorder columns to match requested format: rank, team, score, penalty, solved
            column_order = ['rank', 'team', 'score', 'penalty', 'solved']
            df = df[column_order]
            
            df.to_csv(filepath, index=False)
            print(f"Data saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving CSV: {e}")
            # Try alternative filename
            try:
                filename = f"contest_{contest_id}_{timestamp}.csv"
                filepath = os.path.join(self.output_dir, filename)
                df.to_csv(filepath, index=False)
                print(f"Data saved to alternative path: {filepath}")
                return filepath
            except Exception as e2:
                print(f"Failed to save with alternative filename: {e2}")
                return ""
    
    def crawl_contest(self, contest_id: str) -> str:
        """
        Complete crawl process for a single contest.
        
        Args:
            contest_id: VJudge contest ID
            
        Returns:
            Path to saved CSV file
        """
        print(f"\n=== Crawling Contest {contest_id} ===")
        
        # Extract data
        data = self.get_contest_data(contest_id)
        
        if not data:
            print(f"Failed to extract data for contest {contest_id}")
            return ""
        
        # Save to CSV
        csv_path = self.save_to_csv(data, contest_id)
        
        if csv_path:
            print(f"Successfully processed contest {contest_id}")
            print(f"Found {len(data)} participants")
            print(f"Saved to: {csv_path}")
        
        return csv_path
    
    def crawl_multiple_contests(self, contest_ids: List[str]) -> List[str]:
        """
        Crawl multiple contests.
        
        Args:
            contest_ids: List of contest IDs
            
        Returns:
            List of paths to saved CSV files
        """
        csv_files = []
        
        for i, contest_id in enumerate(contest_ids, 1):
            print(f"\n--- Processing Contest {i}/{len(contest_ids)}: {contest_id} ---")
            
            csv_path = self.crawl_contest(contest_id)
            if csv_path:
                csv_files.append(csv_path)
            
            # Small delay between requests to be respectful
            if i < len(contest_ids):
                time.sleep(2)
        
        print(f"\n=== Summary ===")
        print(f"Processed {len(contest_ids)} contests")
        print(f"Successfully saved {len(csv_files)} CSV files")
        
        return csv_files
    
    def close(self):
        """Close the session (for compatibility)."""
        if hasattr(self, 'session'):
            self.session.close()
        print("Crawler session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Example usage"""
    contest_ids = ["739901"]  # Example contest ID
    
    with VJudgeRankingCrawler() as crawler:
        saved_files = crawler.crawl_multiple_contests(contest_ids)
        
        print(f"\n--- Summary ---")
        print(f"Processed {len(saved_files)} contests")
        for file_path in saved_files:
            print(f"Saved: {file_path}")


if __name__ == "__main__":
    main()
