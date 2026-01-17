import asyncio
import aiohttp

async def fetch(url):
    """Fetch the content of a URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            print(f"{url} downloaded: {len(text)} bytes")
            return text

async def main():
    urls = [
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.github.com",
    ]
    # Run all fetches concurrently
    results = await asyncio.gather(*(fetch(url) for url in urls))
    print("All downloads complete.")

if __name__ == "__main__":
    asyncio.run(main())
