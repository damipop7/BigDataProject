import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
import os
import logging
from src.data_collection import DataCollector
from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTrainer

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Initialize Spark session with proper configuration"""
    return SparkSession.builder \
        .appName("SoccerAnalytics") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED") \
        .getOrCreate()

def main():
    try:
        # Ensure directories exist
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("models", exist_ok=True)

        # Initialize Spark
        spark = create_spark_session()
        
        # Initialize pipeline components
        data_collector = DataCollector()
        processor = DataProcessor(spark)
        feature_engineer = FeatureEngineer(spark)
        model_trainer = ModelTrainer(spark)

        # Execute pipeline
        logger.info("Starting data collection...")
        data_collector.collect_all_data()

        logger.info("Processing data...")
        match_data = processor.load_and_clean_match_data()
        
        logger.info("Engineering features...")
        featured_data = feature_engineer.create_team_features(match_data)
        
        logger.info("Training model...")
        model, test_data = model_trainer.train_model(featured_data)
        
        # Save model and evaluate
        model.save("models/match_prediction_model")
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise
    finally:
        if 'spark' in locals():
            spark.stop()

if __name__ == "__main__":
    main()