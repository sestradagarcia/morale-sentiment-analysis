import re
import json
import sys

# Add the parent directory to the system path to import miro_api
sys.path.append('..')  # Adjust this if necessary to point to the correct location

# Import the Miro API function
from miro_api import get_miro_items

def clean_text(text):
    """
    Function to clean the raw text by:
    - Removing HTML tags
    - Converting to lowercase
    - Removing special characters
    - Trimming excessive whitespace
    """
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', '', text)

    # Convert to lowercase
    cleaned = cleaned.lower()

    # Remove special characters and excessive whitespace
    cleaned = re.sub(r'[^a-zA-Z\s]', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

def main():
    # Get the response from Miro API
    response = get_miro_items()

    # Apply regex cleaning to each item in the response
    cleaned_data = []
    for item in response:
        # Clean the text from each item
        cleaned_text = clean_text(item['text'])

        # Append the cleaned data with the relevant information
        cleaned_data.append({
            'id': item['id'],
            'type': item['type'],
            'cleaned_text': cleaned_text
        })

    # Save the cleaned data to a JSON file
    with open("cleaned_data.json", "w") as f:
        json.dump(cleaned_data, f, indent=2)

    print("Cleaned data saved to 'cleaned_data.json'")

if __name__ == "__main__":
    main()
