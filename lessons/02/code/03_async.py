import asyncio
from typing import List, Sequence, Awaitable
import aiohttp
from aiohttp import ClientSession


# Async function to fetch a URL
async def fetch_url(session: ClientSession, url: str) -> None:
    # Send HTTP GET request (non-blocking)
    # The event loop can switch to other tasks while waiting for response
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")


# Main async function
async def main() -> None:
    # List of URLs (same URL repeated 3 times)
    # Each request has a delay of ~1 second (simulated by httpbin)
    urls: List[str] = ["https://httpbin.org/delay/1"] * 3

    # Create a single shared HTTP session
    # Reusing session is efficient (connection pooling)
    async with aiohttp.ClientSession() as session:

        # Create coroutine tasks (but do not run them yet)
        tasks: Sequence[Awaitable[None]] = [fetch_url(session, url) for url in urls]

        # Run all tasks concurrently
        # asyncio.gather schedules and executes them together
        await asyncio.gather(*tasks)


# Start the event loop and run main()
asyncio.run(main())
