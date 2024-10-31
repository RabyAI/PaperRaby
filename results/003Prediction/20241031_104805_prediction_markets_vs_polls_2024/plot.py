import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Read and parse the data from notes.txt
with open('notes.txt', 'r') as f:
    content = f.read()
    
# Extract the JSON data between Results: and Description:
start = content.find('Results: ') + 9
end = content.find('Description:')
data_str = content[start:end].strip()
data = json.loads(data_str)

# Convert the list of dictionaries into usable data
dates = []
polling_harris = []
polling_trump = []
market_harris = []
market_trump = []

for entry in data:
    # Extract the data from the nested dictionary structure
    row = list(entry.values())[0]  # Get the inner string
    parts = row.split('\t')
    
    # Parse date
    date = datetime.strptime(parts[0], '%m/%d/%y')
    dates.append(date)
    
    # Extract values
    polling_harris.append(float(parts[1]))
    polling_trump.append(float(parts[2]))
    market_harris.append(float(parts[3]))
    market_trump.append(float(parts[4]))

# Create the visualization
plt.figure(figsize=(15, 10))

# Plot polling data
plt.plot(dates, polling_harris, 'b-', label='Harris Polling', linewidth=2)
plt.plot(dates, polling_trump, 'r-', label='Trump Polling', linewidth=2)

# Plot prediction market data
plt.plot(dates, market_harris, 'b--', label='Harris Prediction Market', linewidth=2)
plt.plot(dates, market_trump, 'r--', label='Trump Prediction Market', linewidth=2)

# Customize the plot
plt.title('Polling vs Prediction Markets: 2024 Presidential Election', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Support (%)', fontsize=12)

# Format x-axis to show dates nicely
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
plt.xticks(rotation=45)

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend(fontsize=10)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('election_analysis.png', dpi=300, bbox_inches='tight')
