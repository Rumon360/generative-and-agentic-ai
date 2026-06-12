import sys
import time
import math
import os
import threading


def _wave_loop(stop_event):
    width = min(25, os.get_terminal_size().columns - 2)
    frame = 0
    chars = " ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    while not stop_event.is_set():
        wave = ""
        for i in range(width):
            index = math.sin((i + frame) * 0.3) * 0.5 + 0.5
            wave += chars[int(index * (len(chars) - 1))]
        sys.stdout.write(f"\r\033[36m{wave}\033[0m")
        sys.stdout.flush()
        frame += 1
        time.sleep(0.05)
    sys.stdout.write("\r" + " " * width + "\r")
    sys.stdout.flush()


_stop_event = None
_thread = None


def start():
    global _stop_event, _thread
    _stop_event = threading.Event()
    _thread = threading.Thread(target=_wave_loop, args=(_stop_event,), daemon=True)
    _thread.start()


def stop():
    global _stop_event, _thread
    if _stop_event and _thread:
        _stop_event.set()
        _thread.join()
        _stop_event = None
        _thread = None
