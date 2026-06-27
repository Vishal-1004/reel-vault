import re
import html

def extract_instagram_meta(content: str):
    """Parses raw HTML content directly from memory."""
    
    title_pattern = r'property="og:title"\s+content=(["\'])(.*?)\1'
    desc_pattern = r'property="og:description"\s+content=(["\'])(.*?)\1'
    url_pattern = r'property="og:url"\s+content=(["\'])(.*?)\1'

    title_match = re.search(title_pattern, content, re.DOTALL)
    desc_match = re.search(desc_pattern, content, re.DOTALL)
    url_match = re.search(url_pattern, content, re.DOTALL)

    title = html.unescape(title_match.group(2)) if title_match else None
    description = html.unescape(desc_match.group(2)) if desc_match else None
    url = url_match.group(2) if url_match else None

    combined_text = f"{title or ''} {description or ''}"
    hashtags = list(set(re.findall(r'#\w+', combined_text)))

    profile_name = None
    if url:
        profile_match = re.search(r'instagram\.com/(?!reel/|reels/|p/|tv/)([^/]+)/', url)
        if profile_match:
            profile_name = profile_match.group(1)

    # Return a dictionary directly!
    return {
        "title": title,
        "description": description,
        "url": url,
        "profile_name": profile_name,
        "hashtags": hashtags
    }