# Updated feature_engineering.py with rolling form calculation
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import logging

class FeatureEngineer:
    def __init__(self, spark_session):
        self.spark = spark_session

    def create_team_features(self, match_data):
        # Create window for rolling stats
        goal_window = Window.partitionBy('home_team_api_id').orderBy('date').rowsBetween(-5, -1)
        result_window = Window.partitionBy('home_team_api_id').orderBy('date').rowsBetween(-5, -1)
        away_result_window = Window.partitionBy('away_team_api_id').orderBy('date').rowsBetween(-5, -1)

        # Rolling goal averages
        match_data = match_data.withColumn(
            'home_team_goal_rolling_avg',
            avg('home_team_goal').over(goal_window)
        ).withColumn(
            'away_team_goal_rolling_avg',
            avg('away_team_goal').over(goal_window)
        )

        # Define match result for home team (1 win, 0 loss, 0.5 draw)
        match_data = match_data.withColumn(
            'home_team_result',
            when(col('home_team_goal') > col('away_team_goal'), 1.0)
            .when(col('home_team_goal') < col('away_team_goal'), 0.0)
            .otherwise(0.5)
        )

        # Rolling form (average of recent results)
        match_data = match_data.withColumn(
            'home_team_form', avg('home_team_result').over(result_window)
        )

        match_data = match_data.withColumn(
            'away_team_result',
            when(col('away_team_goal') > col('home_team_goal'), 1.0)
            .when(col('away_team_goal') < col('home_team_goal'), 0.0)
            .otherwise(0.5)
        )

        match_data = match_data.withColumn(
            'away_team_form', avg('away_team_result').over(away_result_window)
        )

        return match_data
