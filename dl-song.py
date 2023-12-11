import requests
from tqdm import tqdm

# Get the URL of the website
url = "https://pagalnew.com/download320/42040"

# Make a request to the website
response = requests.get(url, stream=True)

# Get the total size of the file
total_size = int(response.headers.get('Content-Length'))

# Create a progress bar
progress_bar = tqdm(total=total_size, desc="Downloading...")

# Write the content to a file
with open("website_content.html", "wb") as f:
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)
        progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()
