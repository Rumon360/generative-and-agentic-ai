import asyncio
from concurrent.futures import ProcessPoolExecutor


# CPU-bound function (runs outside async world)
def encrypt(data):
    # Simulate CPU work (e.g., encryption)
    return f"🔒 {data[::-1]}"


async def main():
    # Get the current event loop
    loop = asyncio.get_running_loop()

    # Create a process pool
    # Each process runs in its own Python interpreter
    with ProcessPoolExecutor() as pool:

        # Run CPU-bound function in a separate process
        # -------------------------------
        # WHY PROCESS POOL:
        # encrypt() is CPU-bound
        # Threads would be limited by the GIL
        #
        # ProcessPoolExecutor:
        # - Runs function in a separate process
        # - Each process has its own GIL → no GIL limitation
        # - Enables true parallel execution on multiple CPU cores
        # -------------------------------
        result = await loop.run_in_executor(
            pool,  # Process pool (not thread pool)
            encrypt,  # CPU-bound function
            "credit_card_1234",  # Input data
        )

        # Print result after process completes
        print(f"{result}")


# Required guard for multiprocessing
if __name__ == "__main__":
    asyncio.run(main())
