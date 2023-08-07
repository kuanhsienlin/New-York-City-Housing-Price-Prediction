import argparse
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import urllib.parse
from fake_useragent import UserAgent
import time
import random
import os
import json
import sys
from pathlib import Path
from get_New_York_state_zipcode_html import get_New_York_state_zipcode_html
from get_New_York_city_zipcodes import get_New_York_city_zipcodes
from get_New_York_city_zipcode_html import get_zipcode_pages
from parse_zipcode_html import parse_zipcode_html
from merge_csv_files import merge_csv_files

def main(input_folder, merged_output_file, sample):   
    
    # Step 1: Get all New York zipcode html
    get_New_York_state_zipcode_html()

    # Step 2: Get New York City zipcode by five boroughs
    get_New_York_city_zipcodes()

    # Step 3: Scrape zipcode website by zipcode and save to html
    get_zipcode_pages(sample)

    # Step 4: Convert zipcode html files to csv
    parse_zipcode_html()

    # Step 5: Merge all demo csv files into one csv
    merge_csv_files(input_folder, merged_output_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Scrape zipcode data")
    parser.add_argument("output_file", nargs='?', default="source3_dataset.csv", help="Specify the output file name")
    parser.add_argument("--sample", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    output_folder_parse_csv = "source3_parse_result"  # Folder to store csv files
    Path(output_folder_parse_csv).mkdir(parents=True, exist_ok=True)

    output_folder_merge_csv = "source3_merge_result"  # Folder to store csv files
    Path(output_folder_merge_csv).mkdir(parents=True, exist_ok=True)

    folder_path = "source3_parse_result/"
    merged_output_file = args.output_file

    main(folder_path, merged_output_file, args.sample)

