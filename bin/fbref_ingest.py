import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from pathlib import Path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np

# Create logs and data directories
Path('logs').mkdir(exist_ok=True)
Path('data/raw').mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/fbref_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FBRefScraper:
    def __init__(self):
        self.base_url = "https://fbref.com/en/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://fbref.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = self._init_session()

    def _init_session(self):
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(self.headers)
        return session
        
    def get_league_stats(self, league_url, season):
        try:
            logger.info(f"Fetching data for {league_url} - Season {season}")
            
            # Add random delay between requests (2-5 seconds)
            time.sleep(2 + 3 * np.random.random())
            
            response = self.session.get(league_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract table data
            stats_table = soup.find('table', {'class': 'stats_table'})
            if not stats_table:
                raise ValueError("Stats table not found on page")
                
            df = pd.read_html(str(stats_table))[0]
            
            # Add season information
            df['Season'] = season
            df['Source_URL'] = league_url
            df['Scrape_Date'] = pd.Timestamp.now()
            
            logger.info(f"Successfully scraped data: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while scraping {league_url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {league_url}: {str(e)}")
            return None

# Test the scraper if run directly
if __name__ == "__main__":
    scraper = FBRefScraper()
    test_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    df = scraper.get_league_stats(test_url, "2023-2024")
    
    if df is not None:
        print(df.head())
        # Save to CSV for testing
        df.to_csv("data/raw/premier_league_test.csv", index=False)