from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import logging

class FeatureEngineer:
    def __init__(self, spark_session):
        self.spark = spark_session

    def create_team_features(self, match_data):
        # Create window specifications for rolling statistics
        window_spec = Window.partitionBy('home_team_api_id')\
                           .orderBy('date')\
                           .rowsBetween(-5, -1)

        # Calculate rolling averages for goals
        match_data = match_data.withColumn(
            'home_team_goal_rolling_avg',
            avg('home_team_goal').over(window_spec)
        )

        # Calculate win ratios
        match_data = match_data.withColumn(
            'home_team_result',
            when(col('home_team_goal') > col('away_team_goal'), 1)
            .when(col('home_team_goal') < col('away_team_goal'), 0)
            .otherwise(0.5)
        )

        return match_data