from multiprocessing import (
    Process,
)  # Allows running tasks in separate processes (true parallelism)
import time  # Used to measure execution time


# Function to simulate CPU-bound task (number crunching)
def crunch_number():
    print(f"Started the count process...")
    count = 0
    # CPU-intensive task
    for _ in range(100_000_000):
        count += 1
    print(f"Ended the count process...")


# Guard needed for safe multiprocessing on Windows and some OS
if __name__ == "__main__":
    start = time.time()  # Record start time

    # Create two separate processes for the same CPU-intensive task
    # Each process has its own Python interpreter and memory space
    p1 = Process(target=crunch_number)
    p2 = Process(target=crunch_number)

    # Start both processes
    # Unlike threads, these can run truly simultaneously on multiple CPU cores
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()

    end = time.time()  # Record end time

    # Print total execution time
    print(f"Total time with multiprocessing is {end - start:.2f} seconds")
