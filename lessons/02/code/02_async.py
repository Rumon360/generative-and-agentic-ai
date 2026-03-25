import asyncio
import time


# Async function (coroutine) to brew chai
async def brew(name) -> None:
    print(f"Brewing {name}")

    # Non-blocking sleep
    # This pauses this coroutine, but allows others to run
    await asyncio.sleep(2)

    print(f"{name} is ready...")


# Main async function
async def main():
    # asyncio.gather runs multiple coroutines concurrently
    # All brew() tasks start almost at the same time
    await asyncio.gather(brew("Masala Chai"), brew("Green Chai"), brew("Ginger Chai"))


# Record start time
start = time.time()

# Run the event loop
# Executes main(), which schedules all coroutines
asyncio.run(main())

# Record end time
end = time.time()

# Total time should be ~2 seconds (not 6)
# because all tasks run concurrently, not sequentially
print(f"Total Time : {end - start:.2f}")
