import random
import aiohttp
from aiohttp_socks import ProxyConnector


async def fetch_with_rotating_proxy(
    url: str,
    proxy_file: str = "fastest.txt",
    timeout: int = 10,
):
    """
    Fetch a URL using a random rotating proxy list.

    Returns:
        (html, proxy_used)
    """

    with open(proxy_file, "r", encoding="utf-8") as f:
        proxies = [
            line.strip().split("|")[0]
            for line in f
            if line.strip()
        ]

    proxy_pool = proxies.copy()
    random.shuffle(proxy_pool)

    for proxy in proxy_pool:
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
                            "Mozilla/5.0 "
                            "(Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 "
                            "(KHTML, like Gecko) "
                            "Chrome/137.0.0.0 Safari/537.36"
                        )
                    },
                ) as resp:
                    if resp.status == 200:
                        return await resp.text(), proxy

        except Exception:
            continue

    return None, None