import asyncio
import threading
import time


# Background thread function
def background_worker():
    while True:
        time.sleep(1)  # Blocking sleep
        print(f"Logging the system health")


# Async function to simulate fetching orders
async def fetch_orders():
    await asyncio.sleep(3)  # Non-blocking sleep
    print("Order fetched")


# Start a daemon thread for background logging
# -------------------------------
# Daemon thread:
# - Runs in background
# - Automatically exits when main program ends
# -------------------------------
threading.Thread(target=background_worker, daemon=True).start()

# Run the async event loop
# fetch_orders() runs concurrently with the background thread
asyncio.run(fetch_orders())
