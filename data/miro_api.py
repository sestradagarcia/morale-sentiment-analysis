import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Miro API details
MIRO_API_TOKEN = os.getenv("MIRO_API_TOKEN")
BOARD_ID = os.getenv("BOARD_ID")

def get_miro_items():
    """
    Fetch all items from a Miro board using the board ID and access token.

    Returns:
        A list of dicts containing content, ID, and type for each board item.
    """
    base_url = f"https://api.miro.com/v2/boards/{BOARD_ID}/items"
    headers = {"Authorization": f"Bearer {MIRO_API_TOKEN}"}
    limit = 50
    cursor = None

    items = []

    while True:
        # Build paginated URL
        url = f"{base_url}?limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"❌ Failed to fetch Miro items: {response.status_code} - {response.text}")

        data = response.json()

        for item in data.get("data", []):
            content = item.get("data", {}).get("content")
            if content:  # Only include items that have content
                items.append({
                    "id": item["id"],
                    "type": item["type"],
                    "text": content
                })

        # Check for more pages
        cursor = data.get("cursor")
        if not cursor:
            break

    return items

# For standalone testing
if __name__ == "__main__":
    miro_items = get_miro_items()
    for item in miro_items:
        print(f"{item['type']} ({item['id']}): {item['text']}")
