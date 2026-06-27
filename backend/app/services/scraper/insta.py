import os
import random
import aiohttp
from aiohttp_socks import ProxyConnector

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROXY_FILE = os.path.join(CURRENT_DIR, "fastest.txt")

async def fetch_with_rotating_proxy(
    url: str,
    proxy_file: str = DEFAULT_PROXY_FILE,
    timeout: int = 10,
    max_retries: int = 5  # <-- Added max_retries parameter
):
    with open(proxy_file, "r", encoding="utf-8") as f:
        proxies = [
            line.strip().split("|")[0]
            for line in f
            if line.strip()
        ]

    proxy_pool = proxies.copy()
    random.shuffle(proxy_pool)

    # Use enumerate to keep track of how many attempts we've made
    for attempt, proxy in enumerate(proxy_pool):
        
        # The Backdoor: If we hit the limit, stop trying and return None
        if attempt >= max_retries:
            print(f"⚠️ Reached max retries ({max_retries}). Bailing out early.")
            break 

        try:
            connector = ProxyConnector.from_url(proxy)
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as session:
                async with session.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/137.0.0.0 Safari/537.36"
                        )
                    },
                ) as resp:
                    if resp.status == 200:
                        return await resp.text(), proxy
        except Exception:
            # If the proxy fails, we just silently continue to the next one
            continue

    # If the loop finishes (or breaks) without returning HTML, it returns None
    return None, None