## Python Multiprocessing with Queues and Value

When working with **CPU-bound tasks** in Python, **multiprocessing** allows true parallel execution by creating **separate processes**. To communicate and share data safely between processes, Python provides **Queues** and **Value/Array**.

---

# 1. 🏗️ Multiprocessing Basics

- **Process** = independent Python interpreter with its own memory space.
- No **Global Interpreter Lock (GIL)** limitations → true parallelism.
- `multiprocessing` module provides tools to create processes and share data.

```python id="v3s2xp"
from multiprocessing import Process
import os

def worker(name):
    print(f"{name} running in PID: {os.getpid()}")

p1 = Process(target=worker, args=("Process-1",))
p2 = Process(target=worker, args=("Process-2",))

p1.start()
p2.start()
p1.join()
p2.join()
```

✅ Output: Each process has **different PID**, running truly in parallel.

---

# 2. 🔄 Inter-Process Communication (IPC)

Since processes **do not share memory**, we need mechanisms to share data safely:

1. **Queue** → FIFO communication channel
2. **Value / Array** → Shared memory for simple data

---

# 3. 📦 Multiprocessing Queue

- **Queue** allows multiple processes to **send/receive messages** safely.
- Thread- and process-safe.

```python id="d9q2bl"
from multiprocessing import Process, Queue

def producer(q):
    for i in range(5):
        q.put(i)
        print(f"Produced {i}")

def consumer(q):
    while not q.empty():
        item = q.get()
        print(f"Consumed {item}")

q = Queue()

p1 = Process(target=producer, args=(q,))
p2 = Process(target=consumer, args=(q,))

p1.start()
p1.join()  # Wait for producer
p2.start()
p2.join()
```

✅ Notes:

- Use `put()` to add items.
- Use `get()` to retrieve items.
- Ideal for **pipeline-style processing**.

---

# 4. 💎 Shared Memory with Value

- **Value** allows sharing **single primitive data types** (int, float, char) between processes.
- Requires `lock` for **synchronized access**.

```python id="t8l2xh"
from multiprocessing import Process, Value
import time

def increment(shared_counter):
    for _ in range(5):
        with shared_counter.get_lock():  # Lock for safe update
            shared_counter.value += 1
        print(f"Counter: {shared_counter.value}")
        time.sleep(0.1)

counter = Value('i', 0)  # 'i' = integer

p1 = Process(target=increment, args=(counter,))
p2 = Process(target=increment, args=(counter,))

p1.start()
p2.start()
p1.join()
p2.join()

print(f"Final Counter: {counter.value}")
```

✅ Notes:

- `Value('i', 0)` → integer initialized to 0
- `get_lock()` ensures **atomic updates**
- Can also use `Array` for **shared lists**

---

# 5. 🔄 Combining Queue and Value

- **Queue** → for passing multiple items asynchronously
- **Value** → for tracking counters or shared flags

```python id="x9m4kt"
from multiprocessing import Process, Queue, Value
import time

def producer(q, counter):
    for i in range(5):
        q.put(i)
        with counter.get_lock():
            counter.value += 1
        print(f"Produced {i}, total items: {counter.value}")
        time.sleep(0.1)

def consumer(q):
    while not q.empty():
        item = q.get()
        print(f"Consumed {item}")

q = Queue()
counter = Value('i', 0)

p1 = Process(target=producer, args=(q, counter))
p2 = Process(target=consumer, args=(q,))

p1.start()
p1.join()
p2.start()
p2.join()
```

✅ Benefit:

- Count of items is **always consistent** via `Value`
- Actual data passed safely via `Queue`

---

# 6. ⚡ Best Practices

1. Always **join producer before consumer** when using finite queues.
2. Use **Queue** for **dynamic or large data**.
3. Use **Value/Array** for **small shared state**.
4. Avoid **sharing mutable objects directly** → causes unpredictable behavior.
5. Prefer **Queue + Value** combination for both **data transfer and state tracking**.

---

# 7. 🧠 Mental Model

```text
Process = independent Python interpreter
Queue   = mailbox to send/receive messages safely
Value   = shared single data item in memory
Array   = shared list in memory
get_lock() = ensures atomic operations on shared data
```

---

# 8. ⚠️ Pitfalls

- Forgetting `join()` → consumer may start before producer finishes.
- Directly sharing Python lists/dicts → **not safe**. Use `Manager().list()` instead.
- Accessing `Value` without lock → **race conditions**.
