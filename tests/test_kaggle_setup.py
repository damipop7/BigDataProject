import pytest
from pathlib import Path
from src.data.kaggle_client import KaggleClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_data_path(tmp_path):
    return tmp_path / "test_data"

def test_kaggle_client_initialization(test_data_path):
    """Test Kaggle client setup and authentication"""
    try:
        client = KaggleClient(test_data_path)
        assert client.api is not None
        logger.info("Kaggle client initialized successfully")
    except Exception as e:
        logger.error(f"Kaggle client initialization failed: {str(e)}")
        raise

def test_dataset_download(test_data_path):
    """Test downloading a small dataset"""
    client = KaggleClient(test_data_path)
    test_dataset = "soccer_db"
    client.download_dataset(test_dataset)
    
    # Verify downloaded files
    expected_file = test_data_path / test_dataset / "database.sqlite"
    assert expected_file.exists(), f"Expected file {expected_file} not found"