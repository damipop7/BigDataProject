# Big Data Analytics in Soccer: Performance Insights and Predictive Modeling
## Oluwadamilola Popoola, Ezequiel Tolosa

# Soccer Analytics Project

## Overview
Data analytics project combining soccer data from Kaggle and FBRef for predictive modeling and analysis.

## Project Structure
```
BigDataProject/
├── data/               # Data storage
│   ├── raw/           # Original data
│   ├── processed/     # Cleaned data
│   └── interim/       # Intermediate processing
├── src/               # Source code
├── logs/              # Log files
├── models/            # Trained models
├── notebooks/         # Jupyter notebooks
└── tests/            # Test files
```

## Setup

### Prerequisites
- Python 3.8+
- pip/conda
- Kaggle account

### Installation
```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Configure Kaggle credentials
python setup_kaggle_credentials.py
```

### Configuration
1. Create `.env` file with:
```
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
FBREF_RATE_LIMIT=3
```

2. Verify setup:
```powershell
python -m pytest tests/test_kaggle_auth.py
```

## Usage
```powershell
# Run data collection
python -m src.data.collector

# Run tests
python -m pytest
```

## Logging System

The `logs/` directory contains all application logs, providing detailed tracking of:

### Log Files
- `fbref_scraper.log`: Tracks web scraping activities
  - Scraping attempts
  - Success/failure status
  - Rate limiting information
  - Data validation results

- `kaggle_download.log`: Documents Kaggle data operations
  - Dataset downloads
  - File verification
  - Authentication status
  - Download progress

- `processing.log`: Records data processing steps
  - Data cleaning operations
  - Feature engineering
  - Data validation
  - Error handling

### Log Format
Each log entry follows this structure:
```
TIMESTAMP - MODULE_NAME - LOG_LEVEL - MESSAGE
```

Example:
```
2025-04-14 09:58:15,795 - fbref_client - INFO - Scraping Premier League data (attempt 1/3)...
```

### Log Levels
- ERROR: Critical issues requiring immediate attention
- WARNING: Potential issues or retries
- INFO: General progress information
- DEBUG: Detailed debugging information

### Log Management
- Logs are automatically rotated daily
- Each log file is limited to 10MB
- Last 30 days of logs are retained
- Sensitive information is automatically redacted

## Contributing
1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

## License
MIT License

## Data Sources
• Data 1: https://www.kaggle.com/datasets/hugomathien/soccer/data
• Data 2: https://www.kaggle.com/datasets/hikne707/big-five-european-soccer-leagues
• Data 3: https://www.kaggle.com/datasets/davidcariboo/player-scores
• Data 4: https://fbref.com/en/

## Project Idea
In this project, we will leverage big data techniques to analyze soccer performance metrics and predict match outcomes. Since soccer generates vast amounts of data—including player tracking, passes, shots, and team formations— we will process large datasets efficiently using big data tools. Our approach involves extracting and cleaning raw match data, structuring it for analysis, and applying machine learning algorithms to identify patterns and make predictions. By utilizing distributed computing and scalable data processing, we will explore how big data enhances decision-making in soccer analytics. The final results will be presented through interactive dashboards that provide insights into player performance, tactical trends, and match predictions, helping analysts, coaches, and fans make data-driven decisions.

## Tools and Technologies
• IDEs: JupyterLab, Visual Studio Code
• Libraries: pandas, os, numpy, matplotlib, sklearn
• Programming Languages: Python and/or R
• Visualization: Tableau

## High-Level Architecture and Methodology
The following diagram highlights the tools and methodology we might incorporate in our project.

## Explanation of the Diagram
• Data Ingestion: Collecting raw soccer data from Kaggle.
• Data Processing: Cleaning and structuring data using big data frameworks.
• Feature Engineering: Extracting relevant KPIs like passing accuracy and expected goals.
• Model Training: Applying machine learning algorithms for match prediction.
• Visualization: Presenting insights using Tableau and interactive dashboards.

## Project Goals
The goal of this project is to apply big data analytics to European soccer data
to extract meaningful insights and enhance match prediction models. We aim
to:
• Identify key performance indicators (KPIs) such as passing accuracy, defensive actions, and expected goals (xG) that influence match outcomes.
• Leverage Apache Spark for distributed computing to ensure efficient processing of large datasets.
• Build accurate machine learning models for forecasting match results.
• Analyze tactical strategies by uncovering patterns in formations, team playstyles, and player contributions.
• Create interactive dashboards to make insights accessible for analysts, coaches, and soccer enthusiasts.

