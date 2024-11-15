import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')  # Using a specific seaborn style that's guaranteed to exist
sns.set_theme(style="whitegrid")  # Modern seaborn styling
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

def load_data(filename="notes.txt"):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('Results:'):
                data = json.loads(line.replace('Results:', '').strip())
                return pd.DataFrame(data)
    return None

def prepare_data(df):
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    
    # List of columns that need comma removal
    comma_cols = [
        'Bitcoin ETF Net Flow (USD)',
        'Bitcoin Price in USD',
        'Bitcoin Active Addresses',
        'Bitcoin Block Size',
        'Bitcoin GoogleTrends'
    ]
    
    # Clean comma columns
    for col in comma_cols:
        df[col] = df[col].str.replace(',', '').astype(float)
    
    # Special handling for Mining Hashrate (has 'K' suffix)
    df['Bitcoin Mining Hashrate'] = df['Bitcoin Mining Hashrate'].str.replace('K', '').astype(float) * 1000
    
    # Special handling for Transactions (has '%' suffix)
    df['Bitcoin Transactions'] = df['Bitcoin Transactions'].str.rstrip('%').astype(float)
    
    return df

def plot_price_and_flows(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot Bitcoin price
    ax1.plot(df['Date'], df['Bitcoin Price in USD'], 'b-', label='Bitcoin Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Bitcoin Price (USD)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    
    # Create second y-axis for ETF flows
    ax2 = ax1.twinx()
    ax2.bar(df['Date'], df['Bitcoin ETF Net Flow (USD)'], alpha=0.3, color='r', label='ETF Net Flow')
    ax2.set_ylabel('ETF Net Flow (USD)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title('Bitcoin Price vs ETF Net Flows')
    plt.tight_layout()
    plt.savefig('price_vs_flows.png')
    plt.close()

def plot_correlation_matrix(df):
    # Select numerical columns
    numeric_cols = ['Bitcoin Price in USD', 'Bitcoin ETF Net Flow (USD)', 
                   'Bitcoin Active Addresses', 'Bitcoin Mining Hashrate', 
                   'Bitcoin Transactions']
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Matrix of Bitcoin Metrics')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()

def plot_volume_profile(df):
    plt.figure(figsize=(12, 6))
    
    # Calculate rolling average of ETF flows
    df['Rolling_Flow'] = df['Bitcoin ETF Net Flow (USD)'].rolling(window=3).mean()
    
    plt.plot(df['Date'], df['Rolling_Flow'], 'g-', label='3-Day Rolling Avg Flow')
    plt.fill_between(df['Date'], df['Rolling_Flow'], alpha=0.3)
    
    plt.xlabel('Date')
    plt.ylabel('ETF Net Flow (USD)')
    plt.title('Bitcoin ETF Flow Volume Profile')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('volume_profile.png')
    plt.close()

def main():
    # Load and prepare data
    df = load_data()
    if df is None:
        print("Error: Could not load data from notes.txt")
        return
    
    df = prepare_data(df)
    
    # Generate plots
    plot_price_and_flows(df)
    plot_correlation_matrix(df)
    plot_volume_profile(df)

if __name__ == "__main__":
    main()
