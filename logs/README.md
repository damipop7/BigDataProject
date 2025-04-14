# Log Directory

This directory contains application logs. Files in this directory (except this README and .gitkeep) are ignored by git.

## Log Files
- `fbref_scraper.log`: Web scraping activity logs
- `kaggle_download.log`: Kaggle data download logs
- `processing.log`: Data processing logs

## Retention Policy
- Logs are rotated daily
- Maximum file size: 10MB
- Retention period: 30 days

## Note
Do not delete this directory or .gitkeep file as they are required for application logging.