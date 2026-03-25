import threading

# Create two separate locks (shared resources)
# Think of these as two "keys" that threads must acquire
lock_a = threading.Lock()
lock_b = threading.Lock()


def task1():
    """
    Task 1 tries to acquire lock_a first, then lock_b.
    """

    # Acquire lock_a
    # If another thread already holds it → this thread will WAIT here
    with lock_a:
        print("Task 1 acquired lock A")

        # Simulate some work (optional but useful for seeing deadlock clearly)
        # time.sleep(1)

        # Now try to acquire lock_b
        # If lock_b is already held by another thread → WAIT
        with lock_b:
            print("Task 1 acquired lock B")

    # Locks are automatically released when exiting 'with' blocks
    # First lock_b is released, then lock_a


def task2():
    """
    Task 2 does the OPPOSITE order:
    lock_b first, then lock_a.
    This difference is what creates the deadlock risk.
    """

    # Acquire lock_b first (different order than task1!)
    with lock_b:
        print("Task 2 acquired lock B")

        # Simulate delay (helps reproduce deadlock more reliably)
        # time.sleep(1)

        # Now try to acquire lock_a
        # If task1 is holding lock_a → this thread will WAIT
        with lock_a:
            print("Task 2 acquired lock A")

    # Locks released automatically here


# Create two threads running different tasks
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

# Start both threads "almost" at the same time
t1.start()
t2.start()

# NOTE: No join() here, but program will still wait
# because these are NON-daemon threads by default

# Possible execution flow that causes DEADLOCK:
#
# 1. t1 acquires lock_a
# 2. t2 acquires lock_b
# 3. t1 tries to acquire lock_b → BLOCKED (t2 has it)
# 4. t2 tries to acquire lock_a → BLOCKED (t1 has it)
#
# Now:
# - t1 is waiting for t2
# - t2 is waiting for t1
#
# → Neither can proceed → DEADLOCK
