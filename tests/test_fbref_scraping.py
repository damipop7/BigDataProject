import pytest
from pathlib import Path
from src.data.fbref_client import FBRefClient
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestFBRefScraping:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Setup test environment"""
        self.test_data_path = tmp_path / "test_data"
        self.test_data_path.mkdir(parents=True, exist_ok=True)
        self.fbref_client = FBRefClient(self.test_data_path)

    def test_client_initialization(self):
        """Test FBRef client initialization"""
        assert self.fbref_client is not None
        assert self.fbref_client.data_path == self.test_data_path

    def test_league_scraping_premier_league(self):
        """Test scraping Premier League data"""
        league_name = "Premier League"
        try:
            output_path = self.fbref_client.scrape_league_data(league_name)
            
            # Basic file checks
            assert output_path.exists(), f"Output file not found at {output_path}"
            assert output_path.stat().st_size > 0, "Output file is empty"
            
            # Data validation
            df = pd.read_csv(output_path)
            assert not df.empty, "DataFrame is empty"
            assert len(df) > 0, "No rows in DataFrame"
            assert "League" in df.columns, "League column missing"
            assert "Country" in df.columns, "Country column missing"
            
            # Log successful scrape
            logger.info(f"Successfully scraped {league_name}")
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"Columns: {df.columns.tolist()}")
            
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    def test_invalid_league_name(self):
        """Test handling of invalid league name"""
        with pytest.raises(ValueError):
            self.fbref_client.scrape_league_data("Invalid League")