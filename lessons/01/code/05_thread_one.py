import threading  # Provides threading for concurrent execution
import time  # Used to simulate delays


# Function to simulate boiling milk
def boil_milk():
    print(f"Boiling Milk...")
    time.sleep(2)  # Simulate time taken to boil milk (I/O-bound/sleep)
    print(f"Milk Boiled")


# Function to simulate toasting a bun
def toast_bun():
    print(f"Toasting Bun...")
    time.sleep(3)  # Simulate time taken to toast a bun (I/O-bound/sleep)
    print(f"Toasting Bun Done")


# -------------------------
# Main program
# -------------------------

# Record start time
start = time.time()

# Create threads for both tasks
# Threads allow tasks to run concurrently (overlapping in time)
t1 = threading.Thread(target=boil_milk)
t2 = threading.Thread(target=toast_bun)

# Start both threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()

# Record end time
end = time.time()

# Total time shows concurrency benefit
# Should be close to max(2, 3) = ~3 seconds, not 5 seconds
print(f"Breakfast is ready in {end - start:.2f} seconds")
