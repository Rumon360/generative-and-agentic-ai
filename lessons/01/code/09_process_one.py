import threading
import time


# CPU-intensive function
def cpu_heavy():
    print(f"Crunching some numbers...")

    total = 0
    # CPU-bound work
    for i in range(10**7):
        total += i

    print("DONE")


# Record start time
start = time.time()

# Create 2 threads running the CPU-heavy function
threads = [threading.Thread(target=cpu_heavy) for _ in range(2)]

# Start threads
[t.start() for t in threads]

# Wait for threads to finish
[t.join() for t in threads]

# Record end time
end = time.time()

# Print total time taken
print(f"Time taken: {end - start:.2f} seconds")
