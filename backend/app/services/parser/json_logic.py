import re

def extract_essential_data(raw_data: dict):
    """
    Takes the raw JSON response from RapidAPI and extracts only the essential keys.
    """
    if not raw_data or raw_data.get("error"):
        return None

    # Safely extract top-level keys
    url = raw_data.get("url")
    source = raw_data.get("source")
    title = raw_data.get("title")
    author = raw_data.get("author")
    like_count = raw_data.get("like_count")

    # Extract full_name from the nested 'owner' dictionary
    owner = raw_data.get("owner", {})
    full_name = owner.get("full_name")

    # Extract hashtags from the title (caption) using regex
    hashtags = []
    if title:
        # Find all words starting with '#', and use set() to remove duplicates
        hashtags = list(set(re.findall(r'#\w+', title)))

    # Search through the 'medias' array to find the audio file URL
    audio_url = None
    medias = raw_data.get("medias", [])
    for media in medias:
        if media.get("type") == "audio":
            audio_url = media.get("url")
            break  # Stop searching once we find the first audio file

    # Return the clean, filtered dictionary
    return {
        "url": url,
        "source": source,
        "title": title,
        "author": author,
        "like_count": like_count,
        "full_name": full_name,
        "hashtags": hashtags,
        "audio": {
            "type": "audio",
            "url": audio_url
        }
    }