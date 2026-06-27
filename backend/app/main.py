import os
import json
from app.services.scraper import fetch_reel_data
from app.services.parser import extract_essential_data

def run_scraper_task(url: str):
    print(f"Fetching data for: {url}...")
    
    # 1. Fetch raw data from RapidAPI
    raw_data = fetch_reel_data(url)
    
    if not raw_data:
        print("❌ Failed to fetch data from API.")
        return
        
    print("✅ Successfully fetched data. Parsing essentials...")

    # 2. Parse out only the keys we care about
    clean_data = extract_essential_data(raw_data)
    
    if not clean_data:
        print("❌ Failed to parse data. API might have returned an error format.")
        return
        
    # 3. Define output path (inside the 'app' directory)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(app_dir, "output.json")
    
    # 4. Save the cleanly parsed JSON to the file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4, ensure_ascii=False)
        
    print(f"💾 Successfully saved parsed response to: {output_path}")
    print("\n--- FINAL PARSED DATA ---")
    print(json.dumps(clean_data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Test URL
    test_url = "https://www.instagram.com/reel/DYKQBUwMxT_/"
    run_scraper_task(test_url)