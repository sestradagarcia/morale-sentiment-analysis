import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

# Load the sentiment results from the JSON file
with open('../../model/sentiment_results.json', 'r') as f:
    data = json.load(f)

# Extract sentiment labels
sentiment_labels = [item['sentiment']['label'] for item in data]

# Count the frequency of each sentiment label
label_counts = Counter(sentiment_labels)

# Pie Chart: Proportion of Sentiment Labels
plt.figure(figsize=(8, 6))
plt.pie(label_counts.values(), labels=label_counts.keys(), autopct='%1.1f%%', colors=['blue', 'orange', 'green'])
plt.title('Proportion of Sentiment Labels')
plt.tight_layout()
plt.savefig('sentiment_pie_chart.png')  # Save the pie chart
plt.close()  # Close the figure to avoid blocking

# Line Chart: Sentiment Trends Over Time (if timestamps are available)
# Assuming each item in the data has a 'timestamp' field
timestamps = [item.get('timestamp', f"Item {i}") for i, item in enumerate(data)]
sentiment_scores = [item['sentiment']['score'] for item in data]

plt.figure(figsize=(10, 6))
plt.plot(timestamps, sentiment_scores, marker='o', linestyle='-', color='blue')
plt.title('Sentiment Trends Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Sentiment Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sentiment_line_chart.png')  # Save the line chart
plt.close()  # Close the figure to avoid blocking

# Stacked Bar Chart: Sentiment and Morale Labels
# Extract morale labels
morale_labels = [item['morale']['label'] for item in data]

# Create a DataFrame for visualization
df = pd.DataFrame({'Sentiment': sentiment_labels, 'Morale': morale_labels})
stacked_counts = df.groupby(['Sentiment', 'Morale']).size().unstack(fill_value=0)

# Plot the stacked bar chart
stacked_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'orange', 'green', 'red'])
plt.title('Sentiment and Morale Labels')
plt.xlabel('Sentiment Label')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('sentiment_morale_stacked_bar_chart.png')  # Save the stacked bar chart
plt.close()  # Close the figure to avoid blocking