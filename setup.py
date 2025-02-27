import requests
from tqdm import tqdm
import pandas as pd
import unicodedata
import re


def slugify(text):
    """
    Convert a string to a slug by:
    - Removing diacritics (e.g., converting 'Đà Nẵng' to 'Da Nang')
    - Lowercasing
    - Replacing non-alphanumeric characters with hyphens
    """
    # Normalize to remove accents
    # Replace special characters Đ and đ with D and d
    text = text.replace('Đ', 'D').replace('đ', 'd')
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower()
    # Replace any non-alphanumeric characters with hyphens and remove extra hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text


# Function to fetch data from the API
def fetch_data(range_start, range_end):
    results = []  # List to store each record as a dictionary
    url = "https://internal-vroute-cmc.vexere.com/v1/goyolo/area/"
    # Provided Bearer token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXAiOjIsInVzciI6ImZlIiwiY2lkIjoiYTRlYWM1MDAtMzYyNC0xMWU1LWFjOWUtMDkxMjRjNjAxMDEzIiwiZXhwIjoxNzQwNTg2OTY1fQ.h_VLiNtafv5CyLVrJDLiC_p__YEI76ybs_01_BSUjnQ"

    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    for i in tqdm(range(range_start,range_end), desc="Fetching data"):
        name = None
        slug = None
        url = f"https://internal-vroute-cmc.vexere.com/v1/goyolo/area/{str(i)}"
        response = requests.get(url, headers=headers)
        # Check if the HTTP request was successful
        if response.status_code == 401:
            print("Token expired")
            return None
        if response.status_code == 200:
            data = response.json()
            # Check if the returned message is "success"
            if data.get("message") == "success":
                # Extract and print the name from the "data" field
                name = data.get("data", {}).get("name")
                # Create a slug from the name, if available.
                slug = slugify(name)
        results.append({"id": i, "name": name, "slug": slug})
    # Convert the list of dictionaries to a DataFrame
    a = pd.DataFrame(results)
    a.to_csv("mapping.csv", index=False)

    return None

if __name__ == "__main__":
    fetch_data(1, 1000)