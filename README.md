# Big Data Analytics in Soccer: Performance Insights and Predictive Modeling
## Authors: Oluwadamilola Popoola, Ezequiel Tolosa

## Overview
Advanced data analytics project combining soccer data from multiple sources (Kaggle and FBRef) to perform comprehensive analysis and predictive modeling of soccer match outcomes and team performance metrics.

## Project Structure
```
BigDataProject/
├── data/                           # Data storage
│   ├── raw/                        # Original data
│   │   ├── soccer_db/             # Kaggle SQLite database
│   │   └── fbref/                 # Scraped FBRef data
│   ├── processed/                  # Cleaned and transformed data
│   │   └── integrated_soccer_data.csv
│   ├── interim/                    # Intermediate processing files
│   └── figures/                    # Generated visualizations
├── src/                           # Source code
│   ├── data/                      # Data processing modules
│   │   ├── collector.py           # Data collection scripts
│   │   ├── cleaner.py            # Data cleaning utilities
│   │   └── integrator.py         # Data integration logic
│   ├── models/                    # Model training and evaluation
│   └── visualization/            # Visualization modules
├── notebooks/                     # Jupyter notebooks
│   ├── exploratory/              # EDA notebooks
│   │   └── EDA.ipynb            # Main EDA notebook
│   └── modeling/                 # Modeling notebooks
├── tests/                        # Test files
├── logs/                         # Application logs
├── requirements.txt              # Project dependencies
├── setup.py                      # Project installation
└── README.md                     # Project documentation
```

## Data Sources
1. Kaggle European Soccer Database
   - Historical match data
   - Team and player statistics
   - Source: https://www.kaggle.com/datasets/hugomathien/soccer/data

2. FBRef Current Season Data
   - Live team standings
   - Advanced statistics (xG, pressing, etc.)
   - Source: https://fbref.com/en/

## Setup and Installation

### Prerequisites
- Python 3.8+
- Git
- Kaggle account
- Virtual environment tool (venv/conda)

### Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/BigDataProject.git
cd BigDataProject
```

2. Create and activate virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

4. Configure Kaggle credentials:
- Create `.env` file in project root:
```
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
FBREF_RATE_LIMIT=3
```

5. Initialize data directories:
```powershell
python setup.py
```

## Usage

### Data Collection and Processing
1. Download Kaggle data:
```powershell
python -m src.data.collector --source kaggle
```

2. Scrape FBRef data:
```powershell
python -m src.data.collector --source fbref
```

3. Integrate data sources:
```powershell
python run_integration.py
```

### Analysis and Visualization
1. Run EDA notebook:
```powershell
jupyter lab notebooks/exploratory/EDA.ipynb
```

2. Generate visualizations:
```powershell
python notebooks/exploratory/EDA.py
```

### Key Features
- Data Integration: Combines historical and current season data
- Advanced Statistics: Expected goals (xG), team performance metrics
- Visualization: Automated plot generation and interactive dashboards
- Performance Analysis: Team and player statistics analysis

## Data Dictionary

### Integrated Dataset Columns
- `team_name`: Team name
- `mp`: Matches played
- `w`: Wins
- `d`: Draws
- `l`: Losses
- `gf`: Goals for
- `ga`: Goals against
- `pts`: Points
- `xg`: Expected goals
- `xga`: Expected goals against
- Additional metrics...

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

### Testing
Run tests:
```powershell
python -m pytest
```

### Logging
- Logs stored in `logs/` directory
- Separate logs for data collection, processing, and analysis
- Log rotation enabled

## Visualization Outputs
All visualizations are saved in `data/figures/`:
- `missing_values.png`: Data quality analysis
- `goals_analysis.png`: Team performance visualization
- `win_rates.png`: League comparison
- `season_trends.png`: Seasonal analysis

## Known Issues and Limitations
1. FBRef rate limiting requires delays between requests
2. Historical data limited to available Kaggle dataset
3. Some advanced statistics only available for recent seasons

## Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

## License
MIT License

## Contact
- Oluwadamilola Popoola - [email]
- Ezequiel Tolosa - [email]

## Acknowledgments
- Kaggle dataset contributors
- FBRef for current season data
- Open-source community

## Future Improvements
1. Real-time data updates
2. Advanced predictive modeling
3. Interactive web dashboard
4. Additional data sources integration