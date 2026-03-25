import asyncio  # Library for writing asynchronous (non-blocking) code


# Define an async function (coroutine)
async def brew_chai():
    print("Brewing Chai...")

    # Non-blocking sleep
    # Instead of pausing the whole program, this allows the event loop
    # to run other tasks while waiting
    await asyncio.sleep(2)

    print("Chai is ready.")


# Run the async function
# asyncio.run() starts an event loop, runs the coroutine, and closes the loop
asyncio.run(brew_chai())
