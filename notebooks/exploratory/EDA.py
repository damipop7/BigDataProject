import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configure visualization settings
plt.style.use('default')
sns.set_theme()
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100

# Set up paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "integrated_soccer_data.csv"
FIGURES_PATH = PROJECT_ROOT / "data" / "figures"

# Create figures directory if it doesn't exist
FIGURES_PATH.mkdir(parents=True, exist_ok=True)

# Load and examine the dataset
print("Loading data...")
try:
    df = pd.read_csv(DATA_PATH)
    print(f"Successfully loaded data from {DATA_PATH}")
except FileNotFoundError:
    print(f"Error: Could not find data file at {DATA_PATH}")
    print("Please ensure the file exists and the path is correct")
    raise

print("\nDataset Overview:")
print("-----------------")
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print("\nData Info:")
print(df.info())

# Basic Statistical Analysis
print("\nBasic Statistics:")
print("----------------")
numerical_cols = ['mp', 'w', 'd', 'l', 'gf', 'ga', 'gd', 'pts', 'pts/mp', 'xg', 'xga']
print(df[numerical_cols].describe())

# Team Performance Analysis
print("\nTeam Performance Analysis:")
print("------------------------")
team_stats = df.groupby('team_name').agg({
    'w': ['mean', 'sum'],
    'l': ['mean', 'sum'],
    'd': ['mean', 'sum'],
    'gf': ['mean', 'sum'],
    'ga': ['mean', 'sum'],
    'pts': ['mean', 'sum']
}).round(2)

print("\nTop 10 Teams by Points:")
print(team_stats.sort_values(('pts', 'sum'), ascending=False).head(10))

def save_plots():
    """Generate and save visualization plots"""
    
    # 1. Goals Analysis
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='gf', y='ga', hue='team_name', alpha=0.6)
    plt.title('Goals Scored vs Goals Conceded by Team')
    plt.xlabel('Goals For')
    plt.ylabel('Goals Against')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'goals_analysis.png')
    plt.close()

    # 2. Points Distribution
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='league', y='pts')
    plt.title('Points Distribution by League')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'points_distribution.png')
    plt.close()

    # 3. Expected vs Actual Goals
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='xg', y='gf', scatter_kws={'alpha':0.5})
    plt.title('Expected Goals vs Actual Goals')
    plt.xlabel('Expected Goals (xG)')
    plt.ylabel('Goals Scored')
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'xg_analysis.png')
    plt.close()

    # 4. Win Rate Analysis
    df['win_rate'] = df['w'] / df['mp']
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='league', y='win_rate')
    plt.title('Win Rate Distribution by League')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'win_rates.png')
    plt.close()

# Generate and save plots
print("\nGenerating visualization plots...")
save_plots()
print(f"Analysis complete. Plots saved in {FIGURES_PATH}")