import os
import asyncio
import json

# Import your services
from app.services.scraper import fetch_with_rotating_proxy
from app.services.parser import extract_instagram_meta

async def process_reel(url: str):
    print(f"Fetching HTML for: {url}...")
    
    # 1. Fetch HTML
    html_content, proxy_used = await fetch_with_rotating_proxy(url)
    
    if not html_content:
        print("❌ Failed to fetch reel. All proxies failed.")
        return
        
    print(f"✅ Success! Fetched using proxy: {proxy_used}")

    # --- SAVE TO FILE FOR VERIFICATION ---
    # This gets the directory of main.py and saves output.html right next to it
    app_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(app_dir, "output.html")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"💾 Raw HTML saved to: {output_path}")
    # --------------------------------------

    print("🧠 Parsing metadata...")
    
    # 2. Parse HTML
    extracted_data = extract_instagram_meta(html_content)
    
    # 3. Format and output
    final_output = {
        "status": "success",
        "proxy_used": proxy_used,
        "data": extracted_data
    }
    
    print("\n--- EXTRACTION RESULT ---")
    print(json.dumps(final_output, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    test_url = "https://www.instagram.com/reels/DaC_92OTA_d/"
    asyncio.run(process_reel(test_url))