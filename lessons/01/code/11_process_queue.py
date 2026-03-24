from multiprocessing import Process, Queue


# Function to prepare chai and send result back via queue
def prepare_chai(queue: Queue) -> None:
    # Put the result into the queue so the main process can read it
    queue.put("Masala Chai is ready")


if __name__ == "__main__":
    # Create a queue for communication between processes
    queue: Queue = Queue()

    # Create a process, passing the queue as an argument
    p: Process = Process(target=prepare_chai, args=(queue,))

    # Start the process
    p.start()

    # Wait for the process to finish
    p.join()

    # Retrieve the result from the queue
    # -------------------------------
    # WHY QUEUE IS NEEDED:
    # Each process has its own memory space, so you cannot directly access variables
    # from a child process in the main process.
    # The Queue provides a safe way to send data back from child to parent.
    # -------------------------------
    print(queue.get())  # Output: Masala Chai is ready
