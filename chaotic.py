import requests
from bs4 import BeautifulSoup
import os

def download_mpeg4(url, directory):
    """Downloads MPEG-4 files from the given URL recursively.

    Args:
        url (str): The URL of the page containing the MPEG-4 files.
        directory (str): The directory where the downloaded files will be saved.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.mp4'):
            filename = os.path.basename(href)
            filepath = os.path.join(directory, filename)

            if not os.path.exists(filepath):
                print(f"Downloading {filename}...")
                mpeg4_response = requests.get(url + href, stream=True)

                if mpeg4_response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in mpeg4_response.iter_content(1024):
                            f.write(chunk)
                else:
                    print(f"Failed to download {filename} (status code: {mpeg4_response.status_code})")
            else:
                print(f"{filename} already exists.")

        elif not href.startswith('#') and not href.startswith('javascript'):  # Check for internal links
            download_mpeg4(url + href, directory)  # Recursive call

if __name__ == '__main__':
    url = 'https://archive.org/details/zoids-chaotic-century-s-01e-03'  # Replace with the actual URL
    directory = 'mpeg4_downloads'  # Create this directory if it doesn't exist
    download_mpeg4(url, directory)
