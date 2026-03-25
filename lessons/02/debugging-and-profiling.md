## 🐞 Debugging and Profiling in Python

### Focus: Race Conditions & Deadlocks

In concurrent programming, bugs are often **non-deterministic**—they don’t appear every time, making them notoriously hard to debug. Two of the most critical issues are:

- **Race Conditions**
- **Deadlocks**

Understanding how to **detect, debug, and prevent** them is essential for writing robust Python programs.

---

# 🔹 1. Race Condition

## 📌 Definition

A **race condition** occurs when:

> Two or more threads access shared data **simultaneously**, and the final outcome depends on the **timing of execution**.

---

## ⚠️ Why It Happens

- Threads share memory
- Operations like `x += 1` are **not atomic**
- Context switching interrupts execution mid-operation

---

## 📌 Example (Race Condition)

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # NOT thread-safe

threads = []

for _ in range(2):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Final Counter:", counter)
```

### 🧠 Expected Output:

```
Final Counter: 200000
```

### ❗ Actual Output:

```
Final Counter: (varies, often less)
```

---

## 🔍 Debugging Race Conditions

### 1. Add Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Track execution order:

```python
logging.debug(f"Counter before: {counter}")
```

---

### 2. Force Context Switching

Introduce delays:

```python
import time
time.sleep(0.0001)
```

👉 Makes race conditions easier to reproduce.

---

### 3. Use Deterministic Testing

Run code multiple times:

```bash
for i in range(100): python script.py
```

---

## 🛠️ Fixing Race Conditions

### ✅ Use Locks

```python
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
```

---

### ✅ Other Synchronization Tools

- `RLock`
- `Semaphore`
- `Queue` (thread-safe by design)

---

# 🔹 2. Deadlock

## 📌 Definition

A **deadlock** occurs when:

> Two or more threads are waiting indefinitely for each other to release resources.

---

## ⚠️ Classic Conditions for Deadlock

All four must hold:

1. Mutual exclusion
2. Hold and wait
3. No preemption
4. Circular wait

---

## 📌 Example (Deadlock)

```python
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()

def task1():
    with lock1:
        print("Task1 acquired lock1")
        time.sleep(1)
        with lock2:
            print("Task1 acquired lock2")

def task2():
    with lock2:
        print("Task2 acquired lock2")
        time.sleep(1)
        with lock1:
            print("Task2 acquired lock1")

t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

t1.start()
t2.start()

t1.join()
t2.join()
```

### ❗ Result:

Program **hangs forever**.

---

## 🔍 Debugging Deadlocks

### 1. Use Thread Dumps

```python
import threading
print(threading.enumerate())
```

---

### 2. Use `faulthandler`

```python
import faulthandler
faulthandler.dump_traceback()
```

👉 Shows where threads are stuck.

---

### 3. Timeout Strategy

```python
lock.acquire(timeout=2)
```

Detect failure instead of blocking forever.

---

## 🛠️ Preventing Deadlocks

### ✅ 1. Lock Ordering (Most Important)

Always acquire locks in the same order:

```python
# Always: lock1 → lock2
```

---

### ✅ 2. Use Timeout

```python
if lock.acquire(timeout=1):
    try:
        # critical section
        pass
    finally:
        lock.release()
```

---

### ✅ 3. Avoid Nested Locks

Reduce complexity:

- Use fewer locks
- Combine resources if possible

---

### ✅ 4. Use Higher-Level Constructs

- `queue.Queue`
- `concurrent.futures.ThreadPoolExecutor`

---

# 🔹 3. Profiling Multithreaded Code

Profiling helps identify:

- Bottlenecks
- Lock contention
- Performance inefficiencies

---

## 📌 Tools for Profiling

### ✅ 1. `cProfile`

```python
import cProfile

def main():
    # your threaded code
    pass

cProfile.run("main()")
```

---

### ✅ 2. `time` Module

```python
import time

start = time.time()
# code
print("Elapsed:", time.time() - start)
```

---

### ✅ 3. Line Profiling (Advanced)

Use `line_profiler`:

```bash
pip install line_profiler
```

---

## ⚠️ Note on Python GIL

Python’s **Global Interpreter Lock (GIL)**:

- Prevents true parallel execution of threads (CPU-bound tasks)
- Does NOT prevent race conditions
- Still requires synchronization

---

# 🔹 4. Key Differences

| Issue     | Race Condition           | Deadlock                |
| --------- | ------------------------ | ----------------------- |
| Nature    | Data inconsistency       | Program freeze          |
| Cause     | Concurrent access        | Circular waiting        |
| Detection | Hard (non-deterministic) | Easier (program hangs)  |
| Fix       | Locks, synchronization   | Lock ordering, timeouts |

---

# 🔚 Final Insight

> **Race conditions corrupt your data silently.
> Deadlocks stop your program loudly.**

Both are dangerous—but require **different debugging mindsets**:

- Race condition → Think **data safety**
- Deadlock → Think **resource dependency**
