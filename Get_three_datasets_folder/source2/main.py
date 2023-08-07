import os
import subprocess
import time
import pandas as pd
import overpy
import random
import csv
import time
import chardet
import sys
import argparse
from merge_csv_files import merge_csv_files
from pathlib import Path
from run_batch_file import run_batches
from run_batch_file import run_batch

def main(start_batch, end_batch, output_file, input_file, sample=False):
    
    # Step 1: Get all New York zipcode html

    if sample:
        #print("1")
        run_batch(start_batch, input_file, sample=True)
    else:
        #print("2")
        run_batches(start_batch, end_batch, input_file)

    print("Merging CSV files...")
    output_folder = "source2/"
    merge_csv_files(output_folder, output_file)
    print("Done!")  

        
    #run_batches(start_batch, end_batch)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="API data acquire")
    parser.add_argument("output_file", nargs='?', default="source2_dataset.csv", help="Specify the output file name")
    parser.add_argument("input_file", nargs='?', default=None, help="Specify the input file from source1 dataset")
    parser.add_argument("--sample", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.input_file is None:
        print("Please provide the input file name (source1 dataset output) and check whether both input and output file name exist and input correctly.")
        sys.exit(1)
    
    start_batch = 0
    end_batch = 200

    print("Running batches...")  
    main(start_batch, end_batch, args.output_file, args.input_file, args.sample)
    
    
