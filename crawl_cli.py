"""
VJudge Contest Ranking Crawler - Command Line Interface
Extract ranking data from VJudge contests using HTTP requests (no browser required)
"""

import argparse
import sys
import os
from typing import List
from vjudge_crawler import VJudgeRankingCrawler


def main():
    parser = argparse.ArgumentParser(
        description="VJudge Contest Ranking Crawler - Extract contest rankings to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crawl_cli.py 739901                    # Single contest
  python crawl_cli.py 739901 740123 740456      # Multiple contests
  python crawl_cli.py 739901 -o custom_output   # Custom output directory
  python crawl_cli.py 739901 -v                 # Verbose output

Note: This version uses HTTP requests - no browser required!
        """
    )
    
    parser.add_argument(
        'contest_ids', 
        nargs='+', 
        help='One or more VJudge contest IDs'
    )
    
    parser.add_argument(
        '-o', '--output', 
        default='output',
        help='Output directory for CSV files (default: output)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='VJudge Crawler 2.0 (HTTP Mode)'
    )
    
    args = parser.parse_args()
    
    # Validate contest IDs
    valid_contest_ids = []
    for contest_id in args.contest_ids:
        if contest_id.isdigit():
            valid_contest_ids.append(contest_id)
        else:
            print(f"Warning: Skipping invalid contest ID: {contest_id} (must be numeric)")
    
    if not valid_contest_ids:
        print("Error: No valid contest IDs provided")
        sys.exit(1)
    
    print("VJudge Contest Ranking Crawler (HTTP Mode)")
    print("=" * 50)
    print(f"Contest IDs: {', '.join(valid_contest_ids)}")
    print(f"Output directory: {args.output}")
    print(f"Mode: HTTP requests (no browser required)")
    print("=" * 50)
    
    try:
        # Initialize crawler
        crawler = VJudgeRankingCrawler(output_dir=args.output)
        
        # Process contests
        successful_files = []
        failed_contests = []
        
        for i, contest_id in enumerate(valid_contest_ids, 1):
            print(f"\n[{i}/{len(valid_contest_ids)}] Processing contest {contest_id}...")
            
            try:
                csv_path = crawler.crawl_contest(contest_id)
                if csv_path:
                    successful_files.append(csv_path)
                    print(f"✓ Success: {os.path.basename(csv_path)}")
                else:
                    failed_contests.append(contest_id)
                    print(f"✗ Failed: Unable to extract data for contest {contest_id}")
            
            except Exception as e:
                failed_contests.append(contest_id)
                print(f"✗ Error: {contest_id} - {str(e)}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
        
        # Close crawler
        crawler.close()
        
        # Summary
        print("\n" + "=" * 50)
        print("CRAWLING SUMMARY")
        print("=" * 50)
        print(f"Total contests processed: {len(valid_contest_ids)}")
        print(f"Successful: {len(successful_files)}")
        print(f"Failed: {len(failed_contests)}")
        
        if successful_files:
            print(f"\nSaved files:")
            for file_path in successful_files:
                print(f"  • {file_path}")
        
        if failed_contests:
            print(f"\nFailed contests: {', '.join(failed_contests)}")
        
        print(f"\nOutput directory: {os.path.abspath(args.output)}")
        
        # Exit code
        exit_code = 0 if not failed_contests else 1
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\nCrawling interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
