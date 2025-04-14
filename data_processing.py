from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, spark_session):
        self.spark = spark_session

    def load_and_clean_match_data(self):
        try:
            # Load the datasets
            match_data = self.spark.read.csv("data/raw/match.csv", header=True)
            player_data = self.spark.read.csv("data/raw/player.csv", header=True)
            
            # Handle missing values
            match_data = match_data.dropna(subset=['home_team_goal', 'away_team_goal'])
            
            # Convert data types
            numeric_columns = ['home_team_goal', 'away_team_goal', 'home_team_api_id', 'away_team_api_id']
            for col_name in numeric_columns:
                match_data = match_data.withColumn(col_name, col(col_name).cast('integer'))
            
            return match_data
        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            raise