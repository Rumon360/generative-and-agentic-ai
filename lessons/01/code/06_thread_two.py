import threading  # Allows running tasks concurrently using threads
import time  # Used to simulate delays


# Function to simulate brewing chai
def prepare_chai(type_of_chai, wait_time):
    print(f"{type_of_chai} chai: Brewing...")  # Start message
    time.sleep(wait_time)  # Simulate brewing time
    print(f"{type_of_chai} chai: Ready.")  # Done message


# -------------------------
# Create threads for different types of chai
# Each thread represents a barista brewing a different chai
# -------------------------
t1 = threading.Thread(target=prepare_chai, args=("Masala Chai", 2))
t2 = threading.Thread(target=prepare_chai, args=("Ginger Chai", 3))

# Record start time
start = time.time()

# Start both threads
# Both chai types begin brewing concurrently
t1.start()
t2.start()

# Wait for both threads to finish
# join() ensures main program waits for each chai to be ready
t1.join()
t2.join()

# Record end time
end = time.time()

# Total time shows concurrency benefit
# Should be close to max(2,3) = ~3 seconds instead of 5 if done sequentially
print(f"Chai is ready in {end - start:.2f} seconds")
