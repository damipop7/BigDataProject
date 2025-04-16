from pyspark.sql import SparkSession
from src.data.integrator import DataIntegrator
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create and configure Spark session"""
    return SparkSession.builder \
        .appName("SoccerDataIntegration") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()

def main():
    spark = None
    try:
        # Initialize Spark
        spark = create_spark_session()
        spark.sparkContext.setLogLevel("WARN")
        
        # Initialize integrator with Spark session
        integrator = DataIntegrator(spark_session=spark)
        
        # Run integration
        integrated_data = integrator.integrate_all_data()
        
        # Show summary
        logger.info("\nIntegration Complete!")
        logger.info(f"Final dataset shape: {integrated_data.shape}")
        
    except Exception as e:
        logger.error(f"Integration failed: {str(e)}")
        raise
    finally:
        if spark:
            spark.stop()

if __name__ == "__main__":
    main()