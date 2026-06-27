import asyncio
from insta import fetch_with_rotating_proxy


async def main():
    html, proxy = await fetch_with_rotating_proxy(
        "https://www.instagram.com/reels/DaC_92OTA_d/"
    )

    if html:
        print("Success:", proxy)

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)
    else:
        print("No proxy worked")


asyncio.run(main())