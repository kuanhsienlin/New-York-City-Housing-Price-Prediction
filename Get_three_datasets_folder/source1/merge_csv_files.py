import pandas as pd
import os
import time

def merge_csv_files(folder_path, output_file):
    files = os.listdir(folder_path)
    csv_files = [f for f in files if f.endswith('.csv')]
    print(csv_files)
    print(f"Found {len(csv_files)} CSV files in {folder_path}")

     # Check if csv_files list is not empty
    if not csv_files:
        print("No CSV files found in the folder. Please try executing main.py again.")
        return

    merged_csv = pd.read_csv(os.path.join(folder_path, csv_files[0]))

    for csv_file in csv_files[1:]:
        #print(f"Processing {csv_file}")
        time.sleep(1)
        current_csv = pd.read_csv(os.path.join(folder_path, csv_file))
        merged_csv = pd.concat([merged_csv, current_csv], ignore_index=True)

    # Create the output folder if it doesn't exist
    #os.makedirs(output_folder, exist_ok=True)

    # Combine the output folder and output file name
    #output_file_path = os.path.join(output_folder, output_file)

    # Save the merged CSV to the output folder
    merged_csv.to_csv(output_file, index=False)

    print("Generate the source1 dataset successfully")
