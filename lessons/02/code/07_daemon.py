# Daemon threads are background threads that automatically
# shut down when the main (non-daemon) program exits

import threading  # Provides tools for working with threads
import time  # Used here to simulate delay (sleep)


def monitor_tea_temp():
    """
    This function will run in a separate thread.
    Since it's an infinite loop, it keeps running forever
    unless the program exits.
    """
    while True:
        print("Monitoring tea temperature")  # Simulated background task
        time.sleep(2)  # Pause for 2 seconds to avoid spamming output


# Create a new thread
# target=monitor_tea_temp → function to run in the thread
# daemon=True → marks this thread as a daemon thread
# Meaning: it will automatically terminate when the main thread ends
t = threading.Thread(target=monitor_tea_temp, daemon=True)

# Start the thread → this begins execution of monitor_tea_temp() in parallel
t.start()

# Main thread continues execution immediately (does NOT wait for daemon thread)
print("Main program done")

# IMPORTANT:
# Since the main thread finishes right after this line,
# the daemon thread may not even get a chance to run much
# before the entire program exits.
