import os
import re
import html
import json

def extract_instagram_meta(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

    # (["\']) captures the opening quote (single or double)
    title_pattern = r'property="og:title"\s+content=(["\'])(.*?)\1'
    desc_pattern = r'property="og:description"\s+content=(["\'])(.*?)\1'
    url_pattern = r'property="og:url"\s+content=(["\'])(.*?)\1'

    title_match = re.search(title_pattern, content, re.DOTALL)
    desc_match = re.search(desc_pattern, content, re.DOTALL)
    url_match = re.search(url_pattern, content, re.DOTALL)

    title = html.unescape(title_match.group(2)) if title_match else None
    description = html.unescape(desc_match.group(2)) if desc_match else None
    url = url_match.group(2) if url_match else None

    # Extract all unique hashtags
    combined_text = f"{title or ''} {description or ''}"
    hashtags = list(set(re.findall(r'#\w+', combined_text)))

    # Extract the profile name from the URL
    profile_name = None
    if url:
        profile_match = re.search(r'instagram\.com/(?!reel/|reels/|p/|tv/)([^/]+)/', url)
        if profile_match:
            profile_name = profile_match.group(1)

    result = {
        "title": title,
        "description": description,
        "url": url,
        "profile_name": profile_name,
        "hashtags": hashtags
    }

    return json.dumps(result, indent=4, ensure_ascii=False)

# --- MODIFIED SECTION ---
if __name__ == "__main__":
    # This gets the exact directory where regex_logic.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # This joins that directory with "output.html"
    file_path = os.path.join(current_dir, "output.html")
    
    json_result = extract_instagram_meta(file_path)
    
    if json_result:
        print("Extraction successful! Saving to output.json...")
        
        output_path = os.path.join(current_dir, "output.json")
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(json_result)
            
        print("Done.")
    json_result = extract_instagram_meta("output.html")
    
    if json_result:
        print("Extraction successful! Saving to output.json...")
        
        # Save the result to output.json
        with open("output.json", "w", encoding="utf-8") as out_file:
            out_file.write(json_result)
            
        print("Done.")