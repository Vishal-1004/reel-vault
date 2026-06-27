import os
import requests
import json
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def fetch_with_alterlab(url: str):
    """
    Scrapes Instagram Reels via AlterLab API.
    
    Source: https://alterlab.io/
    Method: POST request to /api/v1/scrape
    Notes: We use this service to bypass anti-bot protections. 
           It returns the raw HTML of the provided Instagram URL.
    """
    api_url = "https://api.alterlab.io/api/v1/scrape"
    
    # Securely fetch API key and Session Cookie from environment variables
    api_key = os.getenv("ALTERLAB_API_KEY")
    api_session = os.getenv("ALTERLAB_API_SESSION")

    payload = json.dumps({
        "url": url,
        "formats": ["html"]
    })
    
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json',
        'Cookie': f'api_session={api_session}'
    }

    try:
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        
        # Depending on AlterLab's response structure, you may need to parse 
        # the response.json() to get the actual HTML string.
        return response.text
    except Exception as e:
        print(f"Error scraping with AlterLab: {e}")
        return None