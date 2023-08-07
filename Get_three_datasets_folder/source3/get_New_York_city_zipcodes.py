#get New York City zipcode by five boroughs

from bs4 import BeautifulSoup
import csv
from pathlib import Path

def get_New_York_city_zipcodes():

    output_folder_NY_state_zipcode = "new_york_state_zipcode"  # Folder to store html files
    Path(output_folder_NY_state_zipcode).mkdir(parents=True, exist_ok=True)
    
    output_folder_NY_city_zipcode = "new_york_city_zipcode"  # Folder to store html files
    Path(output_folder_NY_city_zipcode).mkdir(parents=True, exist_ok=True)


    with open("NY_sate_zipcode_html/NY_state_zipcode_list.html", "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    #print(soup.prettify())

    zip_code_county_data = []
    list_group_items = soup.find_all("div", class_="list-group-item")

    data_found =False
    for item in list_group_items:
        zip_code_div = item.find("div", class_="col-xs-12 prefix-col1")
        county_div = item.find("div", class_="col-xs-12 prefix-col4")
        
        if zip_code_div and county_div:
            data_found = True
            zip_code = zip_code_div.text.strip()
            county = county_div.text.strip()
            zip_code_county_data.append((zip_code, county))
            
    if not data_found:
        print("A web scraping detection mechanism has been activated. Please switch to mobile hotspot or change your IP and rerun main.py.")
        exit(1)
            
    with open(f"{output_folder_NY_state_zipcode}/new_york_state_zipcode.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ZIP Code", "County"])
        writer.writerows(zip_code_county_data)
        
    selected_counties = [
        "Richmond County",
        "Bronx County",
        "New York County",
        "Kings County",
        "Queens County",
    ]

    new_york_city_zipcodes = [
        (zip_code, county) for zip_code, county in zip_code_county_data if county in selected_counties
    ]

    with open(f"{output_folder_NY_city_zipcode}/new_york_city_zipcode.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ZIP Code", "County"])
        writer.writerows(new_york_city_zipcodes)
        
    print('Get New York City zipcode by five boroughs successfully')
