import os
from kaggle.api.kaggle_api_extended import KaggleApi
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_kaggle_auth():
    try:
        # Check if kaggle.json exists
        kaggle_path = Path.home() / '.kaggle' / 'kaggle.json'
        if not os.path.exists(kaggle_path):
            logger.error(f"kaggle.json not found at {kaggle_path}")
            return False

        # Test authentication
        api = KaggleApi()
        api.authenticate()
        
        # Test by listing competitions (this is a valid API call)
        competitions = api.competitions_list()
        logger.info("Successfully authenticated with Kaggle API")
        return True

    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        logger.info("Please ensure your credentials in .env match your Kaggle API token")
        return False

if __name__ == "__main__":
    test_kaggle_auth()