import os
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_kaggle_credentials():
    """Set up Kaggle credentials in the correct location"""
    try:
        # Create .kaggle directory in user's home
        kaggle_dir = Path.home() / '.kaggle'
        kaggle_dir.mkdir(exist_ok=True)
        
        # Path to credentials file
        creds_file = kaggle_dir / 'kaggle.json'
        
        if not creds_file.exists():
            # Create credentials from environment variables or input
            credentials = {
                "username": input("Enter your Kaggle username: "),
                "key": input("Enter your Kaggle API key: ")
            }
            
            # Save credentials
            with open(creds_file, 'w') as f:
                json.dump(credentials, f)
            
            # Set file permissions
            os.chmod(str(creds_file), 0o600)
            
            logger.info(f"Credentials saved to: {creds_file}")
        else:
            logger.info("Kaggle credentials file already exists")
            
    except Exception as e:
        logger.error(f"Error setting up Kaggle credentials: {str(e)}")
        raise

if __name__ == "__main__":
    setup_kaggle_credentials()