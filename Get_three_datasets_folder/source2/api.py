import argparse
import overpy
import random
import csv
import time
from pathlib import Path
import chardet
import sys
import os


api = overpy.Overpass()

def try_api_query(req):
    try:
        return api.query(req)
    except Exception as e:
        print(f"Error: {e}")
        return try_api_query(req)

def fetch_facilities(lat, lon, radius=1000):
    facilities = {
        'Subway': 'railway=subway_entrance',
        'School': 'amenity=school',
        'Park': 'leisure=park',
        'Metro': 'railway=station',
        'Bus': 'highway=bus_stop',
        'Supermarket': 'shop=supermarket',
        'Bank': 'amenity=bank',
        'Parking':'amenity=parking',
        'Cinema':'amenity=cinema',
        'Mall':'shop=mall',
        'Restaurant':'amenity=restaurant',
        'Gym':'amenity=gym',
        'Boutique':'shop=boutique',
        'Museum':'tourism=museum',
        'Arts':'amenity=arts_centre',
        'Theatre':'amenity=theatre'
    }

    facility_counts = {k:0 for k in facilities}
    
    query = f"""
    [out:json];
    node(around:{radius},{lat},{lon});
    out;
    """
    s0 = time.time()
    result = try_api_query(query)
    #print(time.time()-s0)
    for node in result.nodes:
        for facility, tag in facilities.items():
            k, v = tag.split('=')
            if k in node.tags and node.tags[k] == v:
                facility_counts[facility] += 1
    #print()
    #print(facility_counts)
    # time.sleep(1)  # Sleep for 6 seconds to avoid exceeding the API limit

    return facility_counts

current_file_path = os.path.abspath(__file__)
current_folder = os.path.dirname(current_file_path)
#print("current folder:",current_folder)
parent_folder = os.path.dirname(current_folder)
#print("parent folder:",parent_folder)
input_folder_save = os.path.join(parent_folder, 'source1')
#print("input folder:",input_folder_save)

#input_file = "source1_dataset.csv"  # Your input CSV file
#input_file = os.path.join(input_folder_save, 'source1_dataset.csv')
input_file = os.path.join(input_folder_save, sys.argv[3])
output_folder = "source2/"  # Folder to store output CSV files

Path(output_folder).mkdir(parents=True, exist_ok=True)

# Detect input file encoding
with open(input_file, 'rb') as f:
    result = chardet.detect(f.read())

input_encoding = result['encoding']
start = time.time()


parser = argparse.ArgumentParser()
parser.add_argument("start_pos", type=int)
parser.add_argument("output_file", type=str)
parser.add_argument("sample", type=lambda x: x.lower() == 'true')
args = parser.parse_args()

start_pos = args.start_pos
output_file = args.output_file
sample = args.sample

start_pos = int(sys.argv[1])
sample = sys.argv[2] == 'True'
with open(input_file, newline='', encoding=input_encoding) as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

    #end_pos = start_pos + 5 if sample else start_pos + 50 
    
    for index, row in enumerate(rows):
        if index < start_pos:
            continue
        if sample and index >= start_pos + 5:
            break
        if not sample and index >= start_pos + 50:
            break
        
        #if index < start_pos:
            #continue
        #if index >= end_pos:
            #break
        lat = float(row['latitude'])
        lon = float(row['longitude'])

        facilities = fetch_facilities(lat, lon)

        # Create a new row dictionary with only latitude, longitude, and facility counts
        new_row = {
            "address": row["address"],
            "latitude": lat,
            "longitude": lon
        }
        for facility, count in facilities.items():
            new_row[f"{facility}_count"] = count

        # Save to a new CSV file every 50 rows
        if index % 50 == 0:
            output_file = f"{output_folder}/output_{index//50}.csv"
            with open(output_file, 'w', newline='') as output_csvfile:
                fieldnames = list(new_row.keys())
                writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
                writer.writeheader()

        # Write row to the output CSV file
        with open(output_file, 'a', newline='') as output_csvfile:
            writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
            writer.writerow(new_row)
        if index % 3000 == 0 and index > 0:
        #     time.sleep(10)
            continue
        print("[%d / %d] %s s passed" % (index+1, len(rows), time.time()-start))
