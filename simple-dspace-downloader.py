import csv
import re
import requests
import os
import sys
import logging

def setup_logger():
    """
    Set up logging configuration.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler
    log_file = "download_logs.txt"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

def extract_strings(csv_file):
    """
    Extract strings following the specified pattern from the CSV file.
    """
    print(f"Extracting strings from the CSV file: {csv_file}...")
    extracted_strings = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for cell in row:
                # Extract strings following the specified pattern
                matches = re.findall(r'(http.*/handle/*/\w*/\w*)', cell)
                extracted_strings.extend(matches)
    print("Strings extracted successfully.")
    return extracted_strings

def fetch_html_content(urls, base_url):
    """
    Fetch HTML content of each URL, filter by regex, and return a set of unique matches with prefix.
    """
    print("Fetching HTML content for each URL...")
    unique_matches = set()  # To store unique matches
    for url in urls:
        print(f"Processing source code for URL: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                matches = re.findall(r'href="/bitstream/handle/\d+/\S*"', response.text)
                for match in matches:
                    truncated_match = base_url + match[6:-1]  # Truncate the match and add prefix
                    unique_matches.add(truncated_match)
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                logging.warning(f"Failed to fetch {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            logging.error(f"Error fetching {url}: {e}")
    print("HTML content fetched successfully.")
    return unique_matches

def download_files(file_urls, download_folder):
    """
    Download files from the provided URLs and save them to the specified folder.
    """
    print("Downloading files...")
    for url in file_urls:
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Extract filename from URL and remove metadata after last "?"
                filename = url.split("/")[-1].rsplit("?", 1)[0]
                # Extract folder name from URL
                folder_name = url.split("/")[-2]
                # Create the folder if it doesn't exist
                folder_path = os.path.join(download_folder, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                # Save the file to the folder
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Downloaded: {filename} into folder {folder_name}")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
                logging.warning(f"Failed to download {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            logging.error(f"Error downloading {url}: {e}")
    print("Files downloaded successfully.")

def main(csv_file, base_url):
    print(f"Starting the download process for CSV file: {csv_file} with base URL: {base_url}...")
    download_folder = os.path.splitext(os.path.basename(csv_file))[0]
    print(f"Creating download folder: {download_folder}")
    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    extracted_strings = extract_strings(csv_file)

    # Fetch HTML content for each extracted URL and get filtered unique matches
    unique_matches = fetch_html_content(extracted_strings, base_url)

    # Download files codified by the links contained in unique_matches
    download_files(unique_matches, download_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <base_url>")
        sys.exit(1)
    csv_file_path = sys.argv[1]
    base_url = sys.argv[2]

    # Set up logging
    setup_logger()

    main(csv_file_path, base_url)
