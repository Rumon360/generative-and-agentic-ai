import threading  # Provides support for threads (concurrency)
import time  # Used to measure execution time


# Function to simulate CPU-intensive task (brewing chai)
def brew_chai():
    # Print which thread is running
    print(f"{threading.current_thread().name} started brewing...")

    count = 0
    # CPU-bound work: just incrementing a number many times
    for _ in range(100_000):
        count += 1

    # Finished message
    print(f"{threading.current_thread().name} finished brewing...")


# Create two threads running the same CPU-bound function
thread1 = threading.Thread(target=brew_chai, name="Barista-1")
thread2 = threading.Thread(target=brew_chai, name="Barista-2")

# Record start time
start = time.time()

# Start both threads
# Threads are concurrent, but Python's GIL prevents true parallel execution for CPU-bound code
thread1.start()
thread2.start()

# Wait for threads to finish
thread1.join()
thread2.join()

# Record end time
end = time.time()

# Print total execution time
print(f"Total time taken: {end - start:.2f} seconds")
