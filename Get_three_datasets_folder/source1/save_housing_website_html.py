#Save_housing_website_html

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import urllib.parse
from pathlib import Path
from fake_useragent import UserAgent
import time
import random
import os


def save_housing_website_html(input_folder, output_folder, sample=False):

    # Read the New York City zipcode file
    df = pd.read_csv(os.path.join(input_folder, 'new_york_city_zipcode.csv'))
    #df = pd.read_csv('new_york_city_zipcode.csv')
    zip_codes = df['ZIP Code']
    if sample:
        zip_codes = zip_codes[:5]  # Limit to first 5 zip codes if sample mode is enabled

    #print(zip_codes)

    # Set User-Agent to avoid being blocked
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    # Set the base URL and start page number
    for zip_code_name in zip_codes:
        print("Current parsing zipcode:", zip_code_name)
        print("Wait for processing")
        base_url = f'https://www.trulia.com/NY/New_York/{zip_code_name}/'

        page_num = 1
        rest_count = 0
        sample_count =1

        # Set a random range of rest times (in seconds)

        min_rest_time = 120
        max_rest_time = 150

        while True:
            if page_num == 20:
                print(f"All pages for zip code {zip_code_name} scraped.")
                break
            
            if sample and sample_count == 2:
                break

            # Generate a random wait time to reduce the chance of being blocked
            #wait_time = random.uniform(13, 23)
            #time.sleep(wait_time)

            # Builds the URL of the current page
            if page_num == 1:
                url = base_url
                print(url)
            else:
                url = base_url + str(page_num) + '_p/'
                print(url)

            # Send HTTP request
            response = requests.get(url, headers=headers)
            print(f'Requesting {url} ...')
            
    
            #Check to see if the HTML title contains 'Page xx'. If it does not, the crawl is considered complete
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text()
            if 'Page' not in title and page_num != 1:
                print('All pages scraped. Stopping scraping ...')
                break

            # Writes the HTML content to a file
            file_name = f'{zip_code_name}_page_{page_num}.html'
            output_file_path = os.path.join(output_folder, file_name)
            #with open(file_name, 'wb') as fout:
            with open(output_file_path, 'wb') as fout:
                fout.write(response.content)
            print(f'Page {page_num} saved as {file_name}.')

            # Take a 10-minute break every 100 pages
            rest_count += 1
            if rest_count == 100:
                rest_time = random.randint(min_rest_time, max_rest_time)
                print(f'Pausing for {rest_time} seconds ...')
                time.sleep(rest_time)
                rest_count = 0

            # add page number
            page_num += 1
            sample_count +=1
            
            # Generate a random wait time to reduce the chance of being blocked
            wait_time = random.uniform(13, 19)
            time.sleep(wait_time)
            
