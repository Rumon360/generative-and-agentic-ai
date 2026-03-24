import threading
import requests
import time
from typing import List


# Function to download content from a URL
def download(url: str) -> None:
    print(f"Starting download from {url}")  # Start message
    response = requests.get(url)  # I/O-bound network request
    print(
        f"Finished downloading from {url}, size: {len(response.content)} bytes"
    )  # Done message


# List of URLs to download
urls: List[str] = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg",
]

# Record start time
start = time.time()

# Create and start threads for each download
threads: List[threading.Thread] = []

for url in urls:
    t = threading.Thread(target=download, args=(url,))
    t.start()  # Thread begins download
    threads.append(t)  # Keep reference to join later

# Wait for all threads to finish
for t in threads:
    t.join()

# Record end time
end = time.time()

# Print total time taken
# Because downloads are I/O-bound, threads allow concurrency → total time much shorter than sequential
print(f"Total time: {end - start:.2f} seconds")
