import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Configure style
plt.style.use('seaborn')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['figure.dpi'] = 100

# Load and parse data
def load_results(filename='notes.txt'):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extract JSON data between Results: and Description:
    start = content.find('Results: ') + 9
    end = content.find('Description:', start)
    json_str = content[start:end].strip()
    
    # Parse JSON and convert to DataFrame
    data = json.loads(json_str)
    df = pd.DataFrame(data)
    
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    
    # Convert string columns to numeric
    numeric_columns = [col for col in df.columns if col != 'Date']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col])
    
    return df

# Dictionary mapping run IDs to labels
labels = {
    '0': 'Baseline Run'
}

def plot_price_trends(df):
    """Plot Bitcoin price trends over time"""
    plt.figure()
    plt.plot(df['Date'], df['Bitcoin Price in USD'])
    plt.title('Bitcoin Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('price_trends.png')

def plot_metric_correlations(df):
    """Plot correlation heatmap of Bitcoin metrics"""
    # Calculate correlations
    numeric_cols = [col for col in df.columns if col != 'Date']
    corr = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Bitcoin Metrics')
    plt.tight_layout()
    plt.savefig('metric_correlations.png')

def plot_volume_metrics(df):
    """Plot normalized volume-related metrics"""
    # Normalize metrics for comparison
    metrics = ['Bitcoin Active Addresses', 'Bitcoin Transactions']
    normalized_df = df[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    plt.figure()
    for metric in metrics:
        plt.plot(df['Date'], normalized_df[metric], label=metric)
    
    plt.title('Normalized Volume Metrics Over Time')
    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('volume_metrics.png')

def plot_technical_metrics(df):
    """Plot normalized technical metrics"""
    metrics = ['Bitcoin Block Size', 'Bitcoin Mining Hashrate']
    normalized_df = df[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    plt.figure()
    for metric in metrics:
        plt.plot(df['Date'], normalized_df[metric], label=metric)
    
    plt.title('Normalized Technical Metrics Over Time')
    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('technical_metrics.png')

def main():
    # Load data
    df = load_results()
    
    # Generate plots
    plot_price_trends(df)
    plot_metric_correlations(df)
    plot_volume_metrics(df)
    plot_technical_metrics(df)

if __name__ == '__main__':
    main()
