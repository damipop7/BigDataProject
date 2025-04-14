# Updated data_processing.py with additional cleaning steps
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
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

            initial_count = match_data.count()
            logger.info(f"Initial match data count: {initial_count}")

            # Handle missing values
            match_data = match_data.dropna(subset=['home_team_goal', 'away_team_goal'])

            # Convert data types
            numeric_columns = ['home_team_goal', 'away_team_goal', 'home_team_api_id', 'away_team_api_id']
            for col_name in numeric_columns:
                match_data = match_data.withColumn(col_name, col(col_name).cast('integer'))

            # Drop duplicates
            match_data = match_data.dropDuplicates()

            # Convert date column
            match_data = match_data.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))

            # Filter invalid scores
            match_data = match_data.filter((col("home_team_goal") >= 0) & (col("away_team_goal") >= 0))
            match_data = match_data.filter((col("home_team_goal") <= 10) & (col("away_team_goal") <= 10))

            final_count = match_data.count()
            logger.info(f"Cleaned match data count: {final_count} (removed {initial_count - final_count} rows)")

            return match_data
        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            raise
