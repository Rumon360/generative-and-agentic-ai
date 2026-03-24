## Threads and Locks in Python (In Depth)

Threads and locks are fundamental to **concurrent programming** in Python. Understanding them deeply helps write **safe, efficient, and deadlock-free code**.

---

# 1. 🏃 What is a Thread?

A **thread** is the **smallest unit of execution** within a process.

- A **process** can have **multiple threads**, sharing:

  - Memory
  - Variables
  - Open files

- Threads are **lightweight** compared to processes.

**Python example:**

```python id="g8d1xa"
import threading

def worker(name):
    print(f"{name} is running")

t1 = threading.Thread(target=worker, args=("Thread-1",))
t2 = threading.Thread(target=worker, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()
```

✅ Output shows **interleaved execution**.

---

# 2. 🛡️ Thread Safety

**Thread safety** means that shared data is accessed in a way that **prevents corruption or unexpected behavior**.

### 2.1 Problem: Race Condition

```python id="ry9p2a"
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(counter)  # Often < 200000
```

❌ Why?
Because `counter += 1` is **not atomic**: it involves **read → modify → write**, which threads can **interleave**, causing lost updates.

---

# 3. 🔒 Locks (Mutexes)

A **lock** (or mutex) ensures that **only one thread executes a critical section at a time**.

### 3.1 Basic Lock

```python id="g9z2rk"
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:       # Acquire lock
            counter += 1 # Critical section

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(counter)  # Always 200000
```

✅ `with lock:` ensures the critical section is **thread-safe**.

---

# 4. ⏱ Lock Operations

| Operation        | Description                                      |
| ---------------- | ------------------------------------------------ |
| `lock.acquire()` | Waits until lock is available, then acquires it  |
| `lock.release()` | Releases the lock for other threads              |
| `with lock:`     | Context manager, automatically acquires/releases |

---

# 5. 🧩 Deadlocks

**Deadlock** occurs when **two or more threads wait indefinitely** for locks held by each other.

### Example:

```python id="o2twvx"
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()

def task1():
    with lock1:
        time.sleep(1)
        with lock2:
            print("Task1 done")

def task2():
    with lock2:
        time.sleep(1)
        with lock1:
            print("Task2 done")

t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

t1.start()
t2.start()
t1.join()
t2.join()
```

❌ Can **deadlock** because `task1` holds `lock1` and waits for `lock2` while `task2` holds `lock2` and waits for `lock1`.

**Avoiding deadlocks:**

1. Acquire locks in **consistent order**.
2. Use **timeout** in `acquire()` method: `lock.acquire(timeout=2)`.

---

# 6. 🔄 Reentrant Locks (RLock)

- **Normal Lock** cannot be acquired multiple times by the same thread.
- **RLock (Reentrant Lock)** allows the **same thread** to acquire it multiple times.

```python id="h9s0fj"
import threading

rlock = threading.RLock()

def recursive_task(n):
    if n <= 0:
        return
    with rlock:
        print(f"n = {n}")
        recursive_task(n-1)

recursive_task(3)
```

✅ Prevents **self-deadlocks** in recursive or nested calls.

---

# 7. ⚡ Condition Variables

A **Condition** is used to **wait for a condition to become true**:

```python id="y0w7fj"
import threading

condition = threading.Condition()
data_ready = False

def producer():
    global data_ready
    with condition:
        print("Producing data...")
        data_ready = True
        condition.notify()  # Wake up waiting thread

def consumer():
    global data_ready
    with condition:
        while not data_ready:
            condition.wait()  # Wait until notified
        print("Data consumed")

t1 = threading.Thread(target=consumer)
t2 = threading.Thread(target=producer)

t1.start()
t2.start()
t1.join()
t2.join()
```

- **Producer** signals the consumer using `notify()`.
- **Consumer** waits until `data_ready` becomes `True`.

---

# 8. 🧠 Mental Model

```text
Thread = lightweight worker inside process
Lock = “do not disturb” sign for critical section
RLock = reusable lock for same thread
Condition = “wait until signal” mechanism
```

---

# 9. ⚠️ Best Practices

1. Minimize the scope of locks to reduce contention.
2. Avoid nested locks whenever possible.
3. Prefer **higher-level constructs**: `queue.Queue` is thread-safe.
4. Use **asyncio** for I/O-heavy concurrency instead of threads.
