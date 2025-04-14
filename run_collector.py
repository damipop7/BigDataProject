from src.data.collector import DataCollector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Initialize and run collector
        collector = DataCollector()
        collector.collect_all_data()
    except Exception as e:
        logging.error(f"Collection failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()