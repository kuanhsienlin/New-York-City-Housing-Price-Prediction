#get all New York zipcode html
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import os
from pathlib import Path

def get_New_York_state_zipcode_html():

    output_folder_NY_zipcode_html = "NY_sate_zipcode_html"  # Folder to store html files
    Path(output_folder_NY_zipcode_html).mkdir(parents=True, exist_ok=True)

    #ua = UserAgent()
    #headers = {'User-Agent': ua.random}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
    }
    url = 'https://www.unitedstateszipcodes.org/ny/#zips-list'
    response = requests.get(url, headers=headers)
    print(f'Requesting {url} ...')

    # Check whether the response content is empty
    if not response.content or response.content.isspace():
        print("The response content is empty. Please switch to mobile hotspot or change your IP and rerun main.py.")
        exit(1)
    
    file_name = f'NY_state_zipcode_list.html'
    output_file_path = os.path.join(output_folder_NY_zipcode_html, file_name)
    #with open(file_name, 'wb') as fout:
    with open(output_file_path, 'wb') as fout:
        fout.write(response.content)
    print(f'NY_state_zipcode_html saved')
