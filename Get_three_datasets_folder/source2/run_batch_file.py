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
from merge_csv_files import merge_csv_files
from pathlib import Path


def run_batches(start_batch, end_batch, input_file):
    for i in range(start_batch, end_batch + 1):
        start = i * 200
        run_batch(start, input_file)

def run_batch(start, input_file, sample=False):
    processes = []
    loop_max = 50 if sample else 200
    for j in range(0, loop_max, 50):
        #cmd = f"python api.py {start + j}"
        cmd = f"python api.py {start + j} {sample} {input_file}"
        process = subprocess.Popen(cmd, shell=True)
        processes.append(process)
        time.sleep(1)
        
    print("Wait for processing. Don't close the command winddow")

    for process in processes:
        process.wait()

    print("Wait for processing. Don't close the command winddow")
