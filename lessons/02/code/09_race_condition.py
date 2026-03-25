import threading

# Shared resource (global variable)
chai_stock = 0


def restock():
    global chai_stock

    # Each thread will try to increment 100,000 times
    for _ in range(100_000):
        # NOT ATOMIC → multiple steps internally:
        # 1. Read chai_stock
        # 2. Add 1
        # 3. Write back
        # If two threads do this at the same time → race condition
        chai_stock += 1


# Create 2 threads running the same function
threads = [threading.Thread(target=restock) for _ in range(2)]

# Start both threads
for t in threads:
    t.start()

# Wait for both threads to finish
for t in threads:
    t.join()

# BUG: This is not an f-string, so it prints literally "{chai_stock}"
print("Chai stock: {chai_stock}")
