# by zipcode save to html

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import urllib.parse 
from fake_useragent import UserAgent
import time
import random
from pathlib import Path

#def get_zipcode_pages():

def get_zipcode_pages(sample=False):

    output_folder = "source3_html/"  # Folder to store output CSV files

    Path(output_folder).mkdir(parents=True, exist_ok=True)
        

    # read NY city zip code
    df = pd.read_csv('new_york_city_zipcode/new_york_city_zipcode.csv')
    #df = pd.read_csv('new_york_state_zipcode/new_york_state_zipcode.csv')
    zip_codes = df['ZIP Code']

    #print(zip_codes)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
    }

    page_num = 1
    rest_count = 1

    max_attempts = 20
    wait_time_between_attempts = 5

    # Set the base URL and start page number
    for index, zip_code_name in enumerate(zip_codes):

        if sample and index >= 5:  # Stop the loop after 5 pages if sample mode is enabled
            break
    
        url = f"https://www.unitedstateszipcodes.org/{zip_code_name}/"


        success = False
        attempts = 0

        while not success and attempts < max_attempts:
        # Send HTTP request
            response = requests.get(url, headers=headers)
            print(f'Requesting {url} ...')

            if response.status_code == 200:
                success = True

            # Writes the HTML content to a file
                file_name = f'{output_folder}/{zip_code_name}_page_{page_num}.html'
                with open(file_name, 'wb') as fout:
                    fout.write(response.content)
                print(f'Page {page_num} saved as {file_name}.')
                print("Wait for processing")
                
            else:  #Request unsuccessful
                print(f"Request failed with status code {response.status_code}. Retrying in {wait_time_between_attempts} seconds...")
                attempts += 1
                time.sleep(wait_time_between_attempts)

        if not success:
            print(f"Failed to fetch {url} after {max_attempts} attempts. Skipping this zipcode.")
            continue
        

        # Set a random range of rest times (in seconds)
        min_rest_time = 100
        max_rest_time = 129

        if page_num == 337:
            print(f"All pages for zip code {zip_code_name} scraped.")
            break

        #  Generate a random wait time to reduce the chance of being blocked
        wait_time = random.uniform(13, 23)
        time.sleep(wait_time)

        # Take a 5-minute break every 20 pages
        if rest_count == 20:
            rest_time = random.randint(min_rest_time, max_rest_time)
            print(f'Pausing for {rest_time} seconds ...')
            time.sleep(rest_time)
            rest_count = 0

        # add page
        rest_count += 1
        page_num += 1
