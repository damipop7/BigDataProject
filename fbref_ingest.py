import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging

class FBRefScraper:
    def __init__(self):
        self.base_url = "https://fbref.com/en/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def get_league_stats(self, league_url, season):
        try:
            response = requests.get(league_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract table data
            stats_table = soup.find('table', {'class': 'stats_table'})
            df = pd.read_html(str(stats_table))[0]
            
            # Add season information
            df['Season'] = season
            
            time.sleep(3)  # Respect rate limiting
            return df
            
        except Exception as e:
            logging.error(f"Error scraping {league_url}: {str(e)}")
            return None