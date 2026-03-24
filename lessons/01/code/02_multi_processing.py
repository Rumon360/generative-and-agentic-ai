from multiprocessing import (
    Process,
)  # Allows running functions in separate processes (true parallelism)
import time  # Used to simulate delays


# Function to simulate brewing chai
def brew_chai(name):
    print(f"Start of {name} chai brewing")
    time.sleep(3)  # Simulate time taken to brew chai
    print(f"End of {name} chai brewing")


# Guard to ensure safe multiprocessing on Windows and other OS
if __name__ == "__main__":
    # Create a list of Process objects
    # Each process runs brew_chai() independently with its own Python interpreter
    chai_makers = [
        Process(target=brew_chai, args=(f"Chai Maker #{i +1}",)) for i in range(3)
    ]

    # Start all processes
    # Each process can run on a separate CPU core → true parallelism
    for p in chai_makers:
        p.start()

    # Wait for all processes to complete before moving on
    # join() ensures the main program pauses until each process finishes
    for p in chai_makers:
        p.join()

    # This line runs only after all chai makers have finished
    print("All chai served")
