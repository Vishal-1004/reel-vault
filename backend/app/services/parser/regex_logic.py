import html
import json
import re

def brute_force_extract(html_content: str, search_term: str):
    """
    Finds the exact HTML tag and greedily extracts everything inside the content attribute.
    """
    idx = html_content.find(search_term)
    if idx == -1:
        return None
        
    start_tag = html_content.rfind('<', 0, idx)
    end_tag = html_content.find('>', idx)
    
    if start_tag == -1 or end_tag == -1:
        return None
        
    tag_text = html_content[start_tag:end_tag+1]
    
    # THE FIX: We use a GREEDY regex (.* instead of .*?) on the isolated tag.
    # This forces it to read all the way to the final quote, ignoring quotes inside the text.
    match = re.search(r'content=(["\'])(.*)\1', tag_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        raw_val = match.group(2)
        return html.unescape(raw_val)
        
    return None

def clean_and_extract_metrics(description: str):
    """
    Cleans unwanted characters from the description and extracts likes/comments.
    """
    if not description:
        return None, None, None
        
    # 1. Clean the text: replace literal "\n" and actual newlines with spaces
    clean_desc = description.replace('\\n', ' ').replace('\n', ' ')
    
    # Normalize extra spaces (turns multiple spaces into a single space)
    clean_desc = " ".join(clean_desc.split())
    
    # 2. Extract Likes (e.g., matches "264K likes" or "500 likes")
    likes = None
    likes_match = re.search(r'([\d,KkMmBb\.]+)\s+likes', clean_desc, re.IGNORECASE)
    if likes_match:
        likes = likes_match.group(1)
        
    # 3. Extract Comments (e.g., matches "5,480 comments")
    comments = None
    comments_match = re.search(r'([\d,KkMmBb\.]+)\s+comments', clean_desc, re.IGNORECASE)
    if comments_match:
        comments = comments_match.group(1)
        
    return clean_desc, likes, comments

def find_in_json(data, target_key):
    """Recursively searches nested JSON for deep metrics."""
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]
        for v in data.values():
            result = find_in_json(v, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_in_json(item, target_key)
            if result is not None:
                return result
    return None

def extract_instagram_meta(content: str):
    
    # ==========================================
    # 1. BASELINE EXTRACTION & CLEANING
    # ==========================================
    title = brute_force_extract(content, "og:title")
    raw_description = brute_force_extract(content, "og:description")
    url = brute_force_extract(content, "og:url")

    # Clean the description and pull out the metrics
    clean_description, desc_likes, desc_comments = clean_and_extract_metrics(raw_description)

    # Extract all unique hashtags
    combined_text = f"{title or ''} {clean_description or ''}"
    hashtags = list(set(re.findall(r'#\w+', combined_text)))

    # Extract profile name
    profile_name = None
    if url:
        profile_match = re.search(r'instagram\.com/(?!reel/|reels/|p/|tv/)([^/]+)/', url)
        if profile_match:
            profile_name = profile_match.group(1)

    result = {
        "title": title,
        "description": clean_description,
        "url": url,
        "profile_name": profile_name,
        "hashtags": hashtags,
        "likes": desc_likes,      # Populated from description
        "comments": desc_comments, # Populated from description
        "views": None,
        "video_url": None,
        "thumbnail": None
    }

    # ==========================================
    # 2. DEEP EXTRACTION (Embedded JSON payload)
    # ==========================================
    script_blocks = re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', content, re.DOTALL)
    
    for block in script_blocks:
        if "shortcode_media" in block or "xdt_shortcode_media" in block:
            try:
                json_data = json.loads(block)
                
                # If we find exact integers in the JSON, they will overwrite the text values (e.g., 264000 instead of "264K")
                likes_node = find_in_json(json_data, 'edge_media_preview_like')
                if likes_node and isinstance(likes_node, dict):
                    result['likes'] = likes_node.get('count', result['likes'])
                
                comments_node = find_in_json(json_data, 'edge_media_to_comment')
                if comments_node and isinstance(comments_node, dict):
                    result['comments'] = comments_node.get('count', result['comments'])
                
                view_count = find_in_json(json_data, 'video_view_count') or find_in_json(json_data, 'play_count')
                if view_count is not None:
                    result['views'] = view_count
                    
                video_url = find_in_json(json_data, 'video_url')
                if video_url:
                    result['video_url'] = video_url
                    
                thumbnail = find_in_json(json_data, 'display_url')
                if thumbnail:
                    result['thumbnail'] = thumbnail
                    
                break 
            except json.JSONDecodeError:
                continue

    return result