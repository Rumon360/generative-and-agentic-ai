from multiprocessing import Process
import time


# CPU-intensive function
def cpu_heavy():
    print(f"Crunching some numbers...")

    total = 0
    for i in range(10**7):
        total += i

    print("DONE")


if __name__ == "__main__":
    start = time.time()

    # Create 2 separate processes for CPU-heavy task
    # -------------------------------
    # NO GIL LIMITATION:
    # Each process runs in its own Python interpreter.
    # Each process has its own Global Interpreter Lock (GIL),
    # so they can execute Python bytecode truly in parallel on separate CPU cores.
    # Unlike threads, the GIL does not block execution across processes.
    # This allows CPU-bound tasks to run simultaneously and finish faster.
    # -------------------------------
    processes = [Process(target=cpu_heavy) for _ in range(2)]

    [p.start() for p in processes]
    [p.join() for p in processes]

    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
