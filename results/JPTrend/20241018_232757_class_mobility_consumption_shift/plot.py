import json
import matplotlib.pyplot as plt
import numpy as np

# Load data from notes.txt
with open('notes.txt', 'r') as f:
    content = f.read()

# Extract the results JSON string
results_start = content.index('[')
results_end = content.index(']', results_start) + 1
results_json = content[results_start:results_end]

# Parse the JSON data
data = json.loads(results_json)

# Prepare data for plotting
years = [int(item['Year']) for item in data]
rich_class = [float(item['Rich Class (%)']) for item in data]
upper_middle_class = [float(item['Upper Middle Class (%)']) for item in data]
lower_middle_class = [float(item['Lower Middle Class (%)']) for item in data]
poor_class = [float(item['Poor Class (%)']) for item in data]
material_consumption = [float(item['Material Consumption']) for item in data]
spiritual_consumption = [float(item['Spiritual Consumption']) for item in data]

# Calculate class mobility indices
def calculate_mobility_index(class_percentages):
    return [class_percentages[i+1] - class_percentages[i] for i in range(len(class_percentages)-1)]

rich_mobility = calculate_mobility_index(rich_class)
upper_middle_mobility = calculate_mobility_index(upper_middle_class)
lower_middle_mobility = calculate_mobility_index(lower_middle_class)
poor_mobility = calculate_mobility_index(poor_class)

# Plot class percentages over time
plt.figure(figsize=(12, 6))
plt.plot(years, rich_class, label='Rich Class')
plt.plot(years, upper_middle_class, label='Upper Middle Class')
plt.plot(years, lower_middle_class, label='Lower Middle Class')
plt.plot(years, poor_class, label='Poor Class')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Class Percentages Over Time')
plt.legend()
plt.grid(True)
plt.savefig('class_percentages.png')
plt.close()

# Plot material and spiritual consumption trends
plt.figure(figsize=(12, 6))
plt.plot(years, material_consumption, label='Material Consumption')
plt.plot(years, spiritual_consumption, label='Spiritual Consumption')
plt.xlabel('Year')
plt.ylabel('Consumption Percentage')
plt.title('Material vs Spiritual Consumption Trends')
plt.legend()
plt.grid(True)
plt.savefig('consumption_trends.png')
plt.close()

# Plot class mobility indices
plt.figure(figsize=(12, 6))
plt.plot(years[1:], rich_mobility, label='Rich Class Mobility')
plt.plot(years[1:], upper_middle_mobility, label='Upper Middle Class Mobility')
plt.plot(years[1:], lower_middle_mobility, label='Lower Middle Class Mobility')
plt.plot(years[1:], poor_mobility, label='Poor Class Mobility')
plt.xlabel('Year')
plt.ylabel('Mobility Index')
plt.title('Class Mobility Indices Over Time')
plt.legend()
plt.grid(True)
plt.savefig('class_mobility.png')
plt.close()

print("Plots have been generated and saved as PNG files.")
