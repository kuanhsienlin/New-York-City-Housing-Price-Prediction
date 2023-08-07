import os
import argparse
from pathlib import Path
from save_housing_website_html import save_housing_website_html
from scrape_housing_data import scrape_housing_data
from merge_csv_files import merge_csv_files

def main(input_folder_save, output_folder_save, output_folder_parse_csv,output_file,sample):
    #save the website html by zipcode
    save_housing_website_html(input_folder_save, output_folder_save, sample)
    print("Start Web scraping data")
    print("Wait for procesiing")

    #scrape housing data from html
    scrape_housing_data(output_folder_parse_csv,sample)

    #all csv to one csv
    merge_csv_files(output_folder_parse_csv, output_file)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Housing data scraper")
    parser.add_argument("output_file", nargs='?', default="source1_dataset.csv", help="Specify the output file name")
    parser.add_argument("--sample", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    current_file_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file_path)
    #print(current_folder)
    parent_folder = os.path.dirname(current_folder)
    #print(parent_folder)
    input_folder_save = os.path.join(parent_folder, 'source3','new_york_city_zipcode')
    #print(input_folder_save)
    
    output_folder_save = "source1_html"  # Folder to store html files
    Path(output_folder_save).mkdir(parents=True, exist_ok=True)
    
    output_folder_parse_csv = "source1_parse_result"  # Folder to store csv files
    Path(output_folder_parse_csv).mkdir(parents=True, exist_ok=True)

    #output_file = 'source1_dataset.csv'
    output_file = args.output_file  
    
    main(input_folder_save, output_folder_save, output_folder_parse_csv,output_file, args.sample)
    print("Done")

