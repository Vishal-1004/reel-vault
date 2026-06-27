import os
import json
import asyncio

# Import your services
from app.services.scraper import fetch_with_alterlab
from app.services.parser import extract_instagram_meta

async def process_reel(url: str):
    print(f"Fetching HTML for: {url} using AlterLab...")
    
    # 1. Fetch HTML
    # AlterLab is synchronous, so we just call it directly
    html_content = fetch_with_alterlab(url)
    
    if not html_content:
        print("❌ Failed to fetch reel from AlterLab.")
        return
        
    print("✅ Success! HTML retrieved.")

    # --- SAVE TO FILE FOR VERIFICATION ---
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
        "data": extracted_data
    }
    
    print("\n--- EXTRACTION RESULT ---")
    print(json.dumps(final_output, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Test URL
    test_url = "https://www.instagram.com/reels/DaDCoIkhp6u/"
    # test_url = "https://www.instagram.com/reels/DaC_92OTA_d/"
    
    # We use asyncio.run because you kept process_reel as an async function
    asyncio.run(process_reel(test_url))