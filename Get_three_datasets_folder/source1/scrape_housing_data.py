#Scrape housing data

import os
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import csv
import json 
        
def scrape_housing_data(output_folder_parse_csv, sample=False):

    def parse_house_html(data, file_path,output_folder_parse_csv, sample=False):

        file_name = os.path.basename(file_path)
        file_name_without_extension = file_name.replace(".html", "")
        #print(file_name_without_extension)
            
        def find_full_locations(json_obj, key="fullLocation"):
            results = []
            if isinstance(json_obj, dict):
                if key in json_obj:
                    #print(json_obj)
                    results.append(json_obj[key])
                for k, v in json_obj.items():
                    results.extend(find_full_locations(v))
            elif isinstance(json_obj, list):
                for item in json_obj:
                    results.extend(find_full_locations(item))
            #print(results)
            return results

        def find_zipcode(json_obj, key="zipCode"):
            results = []
            if isinstance(json_obj, dict):
                if 'fullLocation' in json_obj:
                    if key in json_obj:
                        #print(json_obj)
                        results.append(json_obj[key])
                for k, v in json_obj.items():
                    results.extend(find_zipcode(v))
            elif isinstance(json_obj, list):
                for item in json_obj:
                    results.extend(find_zipcode(item))
            return results


        def find_price(json_obj, keys=("formattedPrice", "formattedPrice")):
            results = []
            def _recursive_search(obj, found_keys):
                nonlocal results
                local_found_keys = found_keys.copy()
                if isinstance(obj, dict):
                    for key in keys:
                        if key in obj:
                            local_found_keys[key] = obj[key] 

                    if local_found_keys.get("formattedPrice") is not None:
                        all_keys_present = True
                        for key in keys:
                            if key not in local_found_keys:
                                all_keys_present = False
                                break

                        if all_keys_present:
                            results.append(local_found_keys["formattedPrice"])

                    for v in obj.values():
                        _recursive_search(v, local_found_keys)
                elif isinstance(obj, list):
                    for item in obj:
                        _recursive_search(item, found_keys)

            _recursive_search(json_obj, {})
            return results


        def find_floorspace(json_obj, keys=("formattedPrice", "floorSpace")):
            results = []
            def _recursive_search(obj, found_keys):
                nonlocal results
                local_found_keys = found_keys.copy()
                if isinstance(obj, dict):
                    for key in keys:
                        if key in obj:
                            local_found_keys[key] = obj[key] 

                    if local_found_keys.get("formattedPrice") is not None:
                        all_keys_present = True
                        for key in keys:
                            if key not in local_found_keys:
                                all_keys_present = False
                                break

                        if all_keys_present:
                            results.append(local_found_keys["floorSpace"])

                    for v in obj.values():
                        _recursive_search(v, local_found_keys)
                elif isinstance(obj, list):
                    for item in obj:
                        _recursive_search(item, found_keys)

            _recursive_search(json_obj, {})
            return results


        def find_bedroom(json_obj, keys=("formattedPrice", "bedrooms")):
            results = []
            def _recursive_search(obj, found_keys):
                nonlocal results
                local_found_keys = found_keys.copy()
                if isinstance(obj, dict):
                    for key in keys:
                        if key in obj:
                            local_found_keys[key] = obj[key] 

                    if local_found_keys.get("formattedPrice") is not None:
                        all_keys_present = True
                        for key in keys:
                            if key not in local_found_keys:
                                all_keys_present = False
                                break

                        if all_keys_present:
                            results.append(local_found_keys["bedrooms"])

                    for v in obj.values():
                        _recursive_search(v, local_found_keys)
                elif isinstance(obj, list):
                    for item in obj:
                        _recursive_search(item, found_keys)

            _recursive_search(json_obj, {})
            return results


        def find_bathroom(json_obj, keys=("formattedPrice", "bathrooms")):
            results = []
            def _recursive_search(obj, found_keys):
                nonlocal results
                local_found_keys = found_keys.copy()
                if isinstance(obj, dict):
                    for key in keys:
                        if key in obj:
                            local_found_keys[key] = obj[key] 

                    if local_found_keys.get("formattedPrice") is not None:
                        all_keys_present = True
                        for key in keys:
                            if key not in local_found_keys:
                                all_keys_present = False
                                break

                        if all_keys_present:
                            results.append(local_found_keys["bathrooms"])

                    for v in obj.values():
                        _recursive_search(v, local_found_keys)
                elif isinstance(obj, list):
                    for item in obj:
                        _recursive_search(item, found_keys)

            _recursive_search(json_obj, {})
            return results

        def find_latitudes_with_full_location(json_obj, target_key="fullLocation"):
            results = []
            if isinstance(json_obj, dict):
                if target_key in json_obj:
                    if 'coordinates' in json_obj and 'latitude' in json_obj['coordinates']:
                        results.append(json_obj['coordinates']['latitude'])
                for k, v in json_obj.items():
                    results.extend(find_latitudes_with_full_location(v, target_key))
            elif isinstance(json_obj, list):
                for item in json_obj:
                    results.extend(find_latitudes_with_full_location(item, target_key))
            return results
        
        def find_longitudes_with_full_location(json_obj, target_key="fullLocation"):
            results = []
            if isinstance(json_obj, dict):
                if target_key in json_obj:
                    if 'coordinates' in json_obj and 'longitude' in json_obj['coordinates']:
                        #print(json_obj)
                        results.append(json_obj['coordinates']['longitude'])
                for k, v in json_obj.items():
                    results.extend(find_longitudes_with_full_location(v, target_key))
            elif isinstance(json_obj, list):
                for item in json_obj:
                    results.extend(find_longitudes_with_full_location(item, target_key))
            return results

        def find_hometype(json_obj, target_address, target_key="tracking"):
            results = []
            if isinstance(json_obj, dict):
                if target_key in json_obj:
                    tracking_list = json_obj[target_key]
                    #print(tracking_list)
                    for item in tracking_list:
                        if item["key"] == "propertyType" and json_obj.get("location", {}).get("fullLocation") == target_address:
                            results.append(item["value"])
                for k, v in json_obj.items():
                    results.extend(find_hometype(v, target_key, target_address))
            elif isinstance(json_obj, list):
                for item in json_obj:
                    results.extend(find_hometype(item, target_key, target_address))
            return results
        
        latitudes_info = find_latitudes_with_full_location(data)
        longitudes_info = find_longitudes_with_full_location(data)

        full_locations = find_full_locations(data)

        zipcode = find_zipcode(data)
        zipcode = zipcode[0:]

        price_info = find_price(data)
        price_info = [price.replace('$', '') for price in price_info]
        price_info = [price2.replace(',', '') for price2 in price_info]
        price_info = [price3.replace('+', '') for price3 in price_info]
        price_info = [int(price4) for price4 in price_info]

        floorspace = find_floorspace(data)
        floorspace_list = []
        for i in floorspace:
            if i is not None:
                floorspace_list.append((i["formattedDimension"]))
            else: 
                floorspace_list.append("None")
        floorspace_list_no_sqft = [item.replace(" sqft", "") if "sqft" in item else item for item in floorspace_list]
        floorspace_list_no_sqft = [sqft2.replace(',', '') if sqft2 != "None" else "None" for sqft2 in floorspace_list_no_sqft]
        floorspace_list_no_sqft = [int(sqft3) if sqft3 != "None" else "None" for sqft3 in floorspace_list_no_sqft]


        bedroom_list=[]
        bedroom_list_no_bd=[]
        bedroom_num = find_bedroom(data)
        for i2 in bedroom_num:
            #print(i2)
            if i2 is not None:
                bedroom_list.append((i2["formattedValue"]))
            else: 
                bedroom_list.append("None")
        #print(bedroom_list)
        for item2 in bedroom_list:
            if "bd" in item2:
                a = item2.replace("bd", "")
                bedroom_list_no_bd.append(a)
            else:
                a=item2
                bedroom_list_no_bd.append(a)
                
        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False
        
        bedroom_list_no_bd = [int(bed3) if is_int(bed3) else bed3 for bed3 in bedroom_list_no_bd]


        bathroom_list=[]
        bathroom_list_no_bd=[]
        bathroom_num = find_bathroom(data)
        for i3 in bathroom_num:
            #print(i2)
            if i3 is not None:
                bathroom_list.append((i3["formattedValue"]))
            else: 
                bathroom_list.append("None")
        #print(bedroom_list)
        for item3 in bathroom_list:
            if "ba" in item3:
                a3 = item3.replace("ba", "")
                bathroom_list_no_bd.append(a3)
            else:
                a3=item3
                bathroom_list_no_bd.append(a3)
        bathroom_list_no_bd = [int(bath3) if is_int(bath3) else bath3 for bath3 in bathroom_list_no_bd]

        if len(full_locations) == len(zipcode) == len(price_info)== len(floorspace_list_no_sqft) == len(bedroom_list_no_bd) == len(bathroom_list_no_bd) == len(latitudes_info) == len(longitudes_info):
            with open(f'{output_folder_parse_csv}/{file_name_without_extension}.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['address', 'zipcode', 'price', 'sqft', 'bedroom', 'bathroom','latitude','longitude', 'Property Type'])
                range_end = 1 if sample else len(full_locations)
                for i in range(range_end):
                #for i in range(len(full_locations)):
                    hometype_list = find_hometype(data,full_locations[i])
                    hometype_name = hometype_list[0]
                    writer.writerow([full_locations[i], zipcode[i], price_info[i], floorspace_list_no_sqft[i], bedroom_list_no_bd[i], bathroom_list_no_bd[i], latitudes_info[i], longitudes_info[i], hometype_name])
                    
    # Set the folder path to search for
    folder_path = 'source1_html/'

    # Lists all the files in the folder
    files = os.listdir(folder_path)
    #print(len(files))

    # Filter out files ending in.html
    html_files = [f for f in files if f.endswith('.html')]
    #print(html_files)

    # Walk through each HTML file
    for html_file in html_files:
        print('Wait for processing')
        file_path = os.path.join(folder_path, html_file)
        #print(file_path)
        with open(file_path, 'rb') as fin:
            soup = BeautifulSoup(fin.read(), 'html.parser')

            #Find the <script> tag with the specified ID
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                
            if script_tag is not None:
                json_str = script_tag.string
                # Continue with json_str
            else:
                print(f"{file_path} The corresponding <script> tag could not be found")


            # Parse a JSON string into a Python object
            data = json.loads(json_str)

            # Data now contains structured JSON data
            #print(data)
            parse_house_html(data, file_path, output_folder_parse_csv,sample) 
