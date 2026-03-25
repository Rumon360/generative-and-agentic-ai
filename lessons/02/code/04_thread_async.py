import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


# Blocking function (not async)
def check_stock(item) -> str:
    print(f"Checking {item} in store...")

    time.sleep(3)  # Blocking operation (simulates slow I/O or computation)

    return f"{item} stock : 42"


# Async main function
async def main():
    # Get the currently running event loop
    loop = asyncio.get_running_loop()

    # Create a thread pool to run blocking code
    with ThreadPoolExecutor() as pool:

        # Run blocking function in a separate thread
        # -------------------------------
        # WHY THIS IS NEEDED:
        # check_stock() uses time.sleep() → blocks execution
        # If we call it directly, it will block the event loop
        #
        # run_in_executor():
        # - Runs blocking function in a separate thread
        # - Keeps event loop free to handle other async tasks
        # -------------------------------
        result = await loop.run_in_executor(
            pool,  # Thread pool
            check_stock,  # Blocking function
            "Masala Chai",  # Argument to function
        )

        # Print result after thread completes
        print(result)


# Start event loop
asyncio.run(main())
