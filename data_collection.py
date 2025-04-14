from data_ingestion.setup import init_spark, download_kaggle_dataset
from data_ingestion.fbref_scraper import FBRefScraper
import os

def main():
    # Create directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Initialize Spark
    spark = init_spark()
    
    # Download Kaggle datasets
    datasets = [
        "hugomathien/soccer",
        "hikne707/big-five-european-soccer-leagues",
        "davidcariboo/player-scores"
    ]
    
    for dataset in datasets:
        download_kaggle_dataset(dataset, "data/raw")
    
    # Initialize FBRef scraper
    scraper = FBRefScraper()
    
    # Example leagues to scrape (you can expand this)
    leagues = {
        "Premier League": "https://fbref.com/en/comps/9/Premier-League-Stats",
        "La Liga": "https://fbref.com/en/comps/12/La-Liga-Stats"
    }
    
    # Scrape current season data
    for league_name, url in leagues.items():
        df = scraper.get_league_stats(url, "2023-2024")
        if df is not None:
            df.to_parquet(f"data/raw/{league_name.lower().replace(' ', '_')}_2023_24.parquet")

if __name__ == "__main__":
    main()