from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
import logging

class ModelTrainer:
    def __init__(self, spark_session):
        self.spark = spark_session

    def prepare_features(self, data):
        # Define feature columns
        feature_columns = [
            'home_team_goal_rolling_avg',
            'away_team_goal_rolling_avg',
            'home_team_form',
            'away_team_form'
        ]

        # Create feature vector
        assembler = VectorAssembler(
            inputCols=feature_columns,
            outputCol="features"
        )

        # Prepare label column
        data = data.withColumn(
            "label",
            when(col("home_team_goal") > col("away_team_goal"), 2)
            .when(col("home_team_goal") < col("away_team_goal"), 0)
            .otherwise(1)
        )

        return assembler, data

    def train_model(self, data):
        # Split data
        train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

        # Initialize model
        rf = RandomForestClassifier(
            labelCol="label",
            featuresCol="features",
            numTrees=100
        )

        # Create pipeline
        pipeline = Pipeline(stages=[assembler, rf])
        model = pipeline.fit(train_data)

        return model, test_data