import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import sys
from datetime import datetime
from contextlib import redirect_stdout

# Try importing optional packages
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    print("Plotly not installed. Interactive visualizations will be skipped.")
    PLOTLY_AVAILABLE = False

try:
    from scipy import stats
    from sklearn.cluster import KMeans
    ADVANCED_STATS_AVAILABLE = True
except ImportError:
    print("scipy/sklearn not installed. Advanced statistics will be skipped.")
    ADVANCED_STATS_AVAILABLE = False

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure visualization settings
plt.style.use('default')
sns.set_theme()
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100

# Set up paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "integrated_soccer_data.csv"
FIGURES_PATH = PROJECT_ROOT / "data" / "figures"
RESULTS_PATH = PROJECT_ROOT / "results"

# Create required directories
FIGURES_PATH.mkdir(parents=True, exist_ok=True)
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

# Load data first
print("Loading data...")
try:
    df = pd.read_csv(DATA_PATH)
    print(f"Successfully loaded data from {DATA_PATH}")
except FileNotFoundError:
    print(f"Error: Could not find data file at {DATA_PATH}")
    print("Please ensure the file exists and the path is correct")
    raise

# Create timestamped results file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = RESULTS_PATH / f"eda_results_{timestamp}.txt"

# Now redirect output to file with loaded data
with open(results_file, 'w') as f:
    with redirect_stdout(f):
        print(f"EDA Results Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*80 + "\n")

        print("Dataset Overview:")
        print("-"*50)
        print(f"Shape: {df.shape}")
        print(f"\nColumns: {df.columns.tolist()}")
        print("\nData Info:")
        df.info()

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

print("\nCalculating performance metrics...")
df['win_rate'] = df['w'] / df['mp']
df['loss_rate'] = df['l'] / df['mp']
df['draw_rate'] = df['d'] / df['mp']
df['goals_per_game'] = df['gf'] / df['mp']
df['goals_conceded_per_game'] = df['ga'] / df['mp']

print("\nTop 10 Teams by Points:")
print(team_stats.sort_values(('pts', 'sum'), ascending=False).head(10))

# Time Series Analysis
print("\nAnalyzing seasonal trends...")
seasonal_trends = df.groupby(['season_x', 'team_name']).agg({
    'pts': 'mean',
    'win_rate': 'mean'
}).unstack()

# Performance Consistency
df['performance_variance'] = df.groupby('team_name')['pts'].transform('std')

# Home vs Away Analysis
print("\nAnalyzing home vs away performance...")
home_away_comparison = df.groupby('team_name').agg({
    'home_team_goal': ['mean', 'std'],
    'away_team_goal': ['mean', 'std']
})

# League Comparison Tests

if ADVANCED_STATS_AVAILABLE:
    # ANOVA test for league differences
    stats.f_oneway(*[group['pts'].values for name, group in df.groupby('league')])

    # Team Performance Consistency
    stats.ttest_ind(df[df['league']=='Premier League']['pts'],
                    df[df['league']=='La Liga']['pts'])

    # Team clustering based on performance metrics
    metrics = df[['pts', 'gf', 'ga', 'xg', 'xga']].values
    kmeans = KMeans(n_clusters=4)
    df['performance_cluster'] = kmeans.fit_predict(metrics)

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

    # 5. Heat Map for Team Performance Metrics
    plt.figure(figsize=(15, 10))
    correlation_matrix = df[['pts', 'gf', 'ga', 'xg', 'xga', 'win_rate']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Heat Map for Team Performance Metrics')
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'team_performance_heatmap.png')
    plt.close()

    # 6. Performance Evolution
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='season_x', y='pts', hue='team_name')
    plt.title('Performance Evolution Over Seasons')
    plt.xlabel('Season')
    plt.ylabel('Points')
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / 'performance_evolution.png')
    plt.close()

    # 7. Distribution Comparisons
    g = sns.FacetGrid(df, col='league', row='season_x', height=4)
    g.map(sns.histplot, 'pts')
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle('Points Distribution Comparisons by League and Season')
    g.savefig(FIGURES_PATH / 'distribution_comparisons.png')
    plt.close()

# Generate and save plots
print("\nGenerating visualization plots...")
save_plots()
print(f"Analysis complete. Plots saved in {FIGURES_PATH}")

# Interactive Plotting Section
if PLOTLY_AVAILABLE:
    try:
        import statsmodels.api as sm
        print("\nGenerating interactive plots...")
        
        # Create scatter plot with trend line
        fig = px.scatter(df, 
            x='xg', 
            y='gf',
            color='league',
            hover_data=['team_name', 'season_x'],
            trendline="ols",
            title='Expected Goals vs Actual Goals by League',
            labels={'xg': 'Expected Goals (xG)', 
                   'gf': 'Goals Scored',
                   'league': 'League'}
        )
        
        # Customize layout
        fig.update_layout(
            template='plotly_white',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Save plot
        print(f"Saving interactive plot to {FIGURES_PATH / 'interactive_goals.html'}")
        fig.write_html(FIGURES_PATH / 'interactive_goals.html')
        
    except ImportError as e:
        print(f"\nWarning: Could not generate interactive plots. Missing dependency: {e}")
        print("Install required package with: pip install statsmodels")
    except Exception as e:
        print(f"\nError generating interactive plot: {e}")
else:
    print("\nSkipping interactive plots (plotly not installed)")