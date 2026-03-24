import threading  # Allows creating threads for concurrent execution
import time  # Used to simulate delays (like real work being done)


# Function to simulate taking orders
def take_orders():
    for i in range(1, 4):
        print(f"Taking order for #{i}")
        time.sleep(1)  # Simulate time delay for taking each order
        # During this sleep, Python can switch to another thread


# Function to simulate brewing chai
def brew_chai():
    for i in range(1, 4):
        print(f"Brewing Chai for #{i}")
        time.sleep(2)  # Simulate longer time for brewing each chai
        # During this sleep, Python can switch to another thread


# Create threads for both tasks
# Each thread allows its function to run concurrently (overlapping in time)
order_thread = threading.Thread(target=take_orders)
brew_thread = threading.Thread(target=brew_chai)

# Start both threads
# Both tasks now begin "at the same time" from a high-level perspective
order_thread.start()
brew_thread.start()

# Wait for both threads to finish before continuing
# join() pauses the main program until the thread completes
order_thread.join()
brew_thread.join()

# This line runs only after both threads have finished
print("All orders taken and chai brewed")
