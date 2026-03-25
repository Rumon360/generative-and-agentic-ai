## Asyncio, Event Loop, Coroutines, and Await in Python

Python’s **asyncio** module enables **asynchronous programming**, allowing you to write **highly concurrent, I/O-bound programs** efficiently. Let’s break down the key concepts in depth.

---

# 1. 🌟 What is Asyncio?

**Asyncio** is Python’s library for **writing concurrent code using the async/await syntax**.

- Handles **many I/O-bound tasks simultaneously** without creating threads or processes.
- Efficient for:

  - Web servers / clients
  - Web scraping
  - Networking
  - Database queries

```python id="z3m4kq"
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World!")

asyncio.run(hello())
```

✅ Notes: `asyncio.run()` starts the **event loop** and runs the coroutine.

---

# 2. 🔄 Event Loop

The **Event Loop** is the **core of asyncio**:

- Continuously runs and **dispatches tasks** (coroutines) that are ready.
- Handles **I/O waiting**, **timers**, and **callbacks**.
- Works in a **single thread** but can manage **thousands of tasks concurrently**.

### Event Loop Example

```python id="f9k1oa"
import asyncio

async def task(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay}s")

async def main():
    await asyncio.gather(
        task("Task-1", 2),
        task("Task-2", 1)
    )

asyncio.run(main())
```

✅ Output is **interleaved**, showing **concurrency without threads**.

---

# 3. 🌀 Coroutines

A **coroutine** is a **special function** that can **pause and resume** execution.

- Declared using `async def`.
- Can use `await` to **pause until an async operation completes**.
- Does **not block the event loop**.

```python id="r7v9wl"
async def greet():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
```

- Calling `greet()` **does not run it immediately**.
- Must be scheduled with:

  - `await greet()` inside another coroutine
  - `asyncio.run(greet())`

---

# 4. ⏳ Await

`await` is used to **pause a coroutine until a result is ready**.

- Only works **inside a coroutine**.
- Releases control to the **event loop** so other tasks can run.

```python id="k2p7dx"
async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # Simulate I/O
    return {"data": 123}

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

✅ Key point: `await` **does not block the program**, it allows **other coroutines to run** during the wait.

---

# 5. 🧩 asyncio.gather() vs asyncio.create_task()

| Function                         | Description                                                                              |
| -------------------------------- | ---------------------------------------------------------------------------------------- |
| `asyncio.gather(*tasks)`         | Runs multiple coroutines concurrently and **waits for all to complete**                  |
| `asyncio.create_task(coroutine)` | Schedules a coroutine to run in the event loop **immediately** and returns a Task object |

```python id="t4j3xs"
async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    task1 = asyncio.create_task(say_after(2, "Hello"))
    task2 = asyncio.create_task(say_after(1, "World"))

    await task1
    await task2

asyncio.run(main())
```

✅ `create_task` allows **fire-and-forget** style scheduling.

---

# 6. ⚡ Real-World Example: Multiple I/O-bound Tasks

```python id="m9k5vb"
import asyncio

async def download_file(name, delay):
    print(f"Starting download: {name}")
    await asyncio.sleep(delay)
    print(f"Finished download: {name}")
    return name

async def main():
    files = ["file1", "file2", "file3"]
    tasks = [download_file(f, i) for i, f in enumerate(files, 1)]
    results = await asyncio.gather(*tasks)
    print("All files downloaded:", results)

asyncio.run(main())
```

- Even though each task **waits for `sleep`**, **all run concurrently**.

---

# 7. 🧠 Mental Model

```text
Event Loop = conductor managing all coroutines
Coroutine = musician who can pause and resume
await = rest periods for the musician to let others play
asyncio.gather() = orchestra performing together
```

---

# 8. ⚠️ Key Points

1. Asyncio is **single-threaded** but highly concurrent.
2. Only **I/O-bound or async libraries** benefit from asyncio.
3. CPU-bound tasks **must use multiprocessing**.
4. Never use **blocking code** inside coroutines (e.g., time.sleep), always use **await asyncio.sleep()**.
5. `await` **pauses the coroutine** but keeps event loop running.

---

# 9. 💡 Pro Tips

- Use `asyncio.run()` for top-level entry point.
- Use `asyncio.create_task()` for background tasks.
- Combine with `aiohttp` or `asyncpg` for real network/database applications.
- Use `asyncio.Queue()` for **producer-consumer patterns**.
