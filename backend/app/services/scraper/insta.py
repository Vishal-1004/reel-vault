import os
import requests
import json
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def fetch_reel_data(reel_url: str):
    """
    Fetches Instagram Reel metadata using the Auto-Download All-In-One API.
    Source: RapidAPI (auto-download-all-in-one)
    """
    url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    payload = json.dumps({"url": reel_url})
    
    headers = {
        'x-rapidapi-key': os.getenv("RAPIDAPI_KEY"),
        'x-rapidapi-host': 'auto-download-all-in-one.p.rapidapi.com',
        'Content-Type': 'application/json',
        'Referer': 'https://reeltoolbox.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        # Return the parsed JSON response
        return response.json()
    except Exception as e:
        print(f"Error fetching from RapidAPI: {e}")
        return None