from multiprocessing import Process, Value
from multiprocessing.sharedctypes import Synchronized
from typing import List


# Function to safely increment a shared counter
def increament(counter: Synchronized) -> None:
    for _ in range(100_000):
        # Acquire the lock associated with the shared Value
        # Ensures that only one process updates counter.value at a time
        with counter.get_lock():
            counter.value += 1


if __name__ == "__main__":
    # Create a shared integer Value initialized to 0
    # 'i' = typecode for signed integer
    # Value creates a shared memory object accessible by multiple processes
    counter: Synchronized = Value("i", 0)

    # Create 4 processes that increment the shared counter
    processes: List[Process] = [
        Process(target=increament, args=(counter,)) for _ in range(4)
    ]

    # Start all processes
    for p in processes:
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Print final counter value
    # Expected: 100_000 * 4 = 400_000
    print(f"Final counter value: {counter.value}")
