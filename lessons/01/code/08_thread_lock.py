import threading

# Shared global variable
counter = 0

# Create a lock object to synchronize access to `counter`
lock = threading.Lock()


# Function to increment the counter
def increament():
    global counter
    for _ in range(100_000):
        # Acquire the lock before modifying the shared variable
        # Ensures that only one thread can change `counter` at a time
        with lock:
            counter += 1


# Create 10 threads that will increment the counter concurrently
threads = [threading.Thread(target=increament) for _ in range(10)]

# Start all threads
[t.start() for t in threads]

# Wait for all threads to finish
[t.join() for t in threads]

# Print the final value of the counter
# Using f-string correctly to include the variable
print(f"Final counter: {counter}")
