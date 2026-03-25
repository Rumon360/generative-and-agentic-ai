# Daemon threads are background threads that automatically
# shut down when the main program exits

import threading
import time


def monitor_tea_temp():
    """
    This function runs in a separate thread.
    It loops forever, printing a message every 2 seconds.
    """
    while True:
        print("Monitoring tea temperature")
        time.sleep(2)


# Create a NON-daemon thread (default behavior)
# daemon=False means:
# → This thread is considered important
# → The program will NOT exit until this thread finishes
t = threading.Thread(target=monitor_tea_temp, daemon=False)

# Start the thread (runs in parallel with main thread)
t.start()

# Main thread finishes quickly
print("Main program done")

# BUT the program does NOT exit here!
# Because the non-daemon thread is still running (infinite loop)
