import json
import matplotlib.pyplot as plt
import numpy as np

# Dictionary mapping run IDs to their labels
labels = {
    "0": "Baseline Assessment"
}

def parse_results(content):
    """Parse the results section from the notes file"""
    start = content.find('[{')
    end = content.find('}]') + 2
    json_str = content[start:end]
    return json.loads(json_str)

def create_bar_plot(data, run_id):
    """Create a bar plot of symptom centrality measures"""
    plt.figure(figsize=(15, 10))
    
    # Sort by centrality value
    sorted_data = sorted(data, key=lambda x: float(x['Depression Node Strength Centrality']), reverse=True)
    
    symptoms = [item['Symptom'] for item in sorted_data]
    centralities = [float(item['Depression Node Strength Centrality']) for item in sorted_data]
    
    # Create bar plot
    plt.bar(range(len(symptoms)), centralities)
    plt.xticks(range(len(symptoms)), symptoms, rotation=45, ha='right')
    plt.ylabel('Depression Node Strength Centrality')
    plt.title(f'Symptom Centrality Measures - {labels[run_id]}')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.savefig(f'centrality_barplot_{run_id}.png')
    plt.close()

def create_network_plot(data, run_id, top_n=10):
    """Create a network-style plot of the top N most central symptoms"""
    plt.figure(figsize=(12, 12))
    
    # Sort and get top N symptoms
    sorted_data = sorted(data, key=lambda x: float(x['Depression Node Strength Centrality']), reverse=True)
    top_symptoms = sorted_data[:top_n]
    
    # Create circular layout
    n_symptoms = len(top_symptoms)
    angles = np.linspace(0, 2*np.pi, n_symptoms, endpoint=False)
    
    # Plot connections to center
    center = (0, 0)
    for i, (symptom, angle) in enumerate(zip(top_symptoms, angles)):
        centrality = float(symptom['Depression Node Strength Centrality'])
        # Calculate point on circle
        x = np.cos(angle)
        y = np.sin(angle)
        
        # Draw line with width proportional to centrality
        plt.plot([center[0], x], [center[1], y], 
                linewidth=centrality*2, alpha=0.6, color='blue')
        
        # Add text label
        text_x = x * 1.2  # Slightly outside the circle
        text_y = y * 1.2
        plt.annotate(symptom['Symptom'], (text_x, text_y),
                    ha='center', va='center')
    
    plt.title(f'Top {top_n} Most Central Symptoms - {labels[run_id]}')
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'network_plot_{run_id}.png')
    plt.close()

def main():
    # Read and parse the notes file
    with open('notes.txt', 'r') as f:
        content = f.read()
    
    # Process each run that has a label
    for run_id in labels.keys():
        data = parse_results(content)
        create_bar_plot(data, run_id)
        create_network_plot(data, run_id)

if __name__ == "__main__":
    main()
