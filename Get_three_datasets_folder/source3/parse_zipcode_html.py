#zipcode html to csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
from pathlib import Path

def parse_zipcode_html():
    def parse_html_file(zip_code, soup, file_path):

        output_folder = "source3_parse_result/"  # Folder to store output CSV files

        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        file_name_without_extension = file_name.replace(".html", "")
        #print(file_name_without_extension)
            
        # Extract median income
        if soup.find("th", text="Median Household Income"):
            median_income_header = soup.find("th", text="Median Household Income")
            median_income = median_income_header.find_next_sibling("td").text
            median_income = median_income.strip('$')
            median_income = median_income.replace(',', '')
            median_income = int(median_income)
        else:
            median_income = None

        # Extract median home value
        if soup.find("th", text="Median Home Value"):
            median_home_value_header = soup.find("th", text="Median Home Value")
            median_home_value = median_home_value_header.find_next_sibling("td").text
            median_home_value = median_home_value.strip('$')
            median_home_value = median_home_value.replace(',', '')
            median_home_value = int(median_home_value)
        else:
            median_home_value = None

        # Extract educational attainment
        if soup.find('h3', text="Educational Attainment For The Population 25 Years And Over"):
            h3 = soup.find('h3', text="Educational Attainment For The Population 25 Years And Over")
            table = h3.find_next('table')
            percentage_elements = table.select('td.text-right:nth-child(3)')
            percentages = [float(item.text[:-1])/100 for item in percentage_elements]
        else:
            percentages = ["None","None","None","None","None","None","None"]
            

        # Extract No Earnings
        if soup.find('span', text='No Earnings'):
            no_earnings_span = soup.find('span', text='No Earnings')
            no_earnings_th = no_earnings_span.find_parent('th')
            no_earnings_value_td, no_earnings_percentage_td = no_earnings_th.find_next_siblings('td')
            no_earnings_value = no_earnings_value_td.text.strip()
            no_earnings_percentage = no_earnings_percentage_td.text.strip()
            # Remove the percent sign, then convert the string to a floating-point number and divide by 100
            no_earnings_decimal = float(no_earnings_percentage.strip('%')) / 100
        else:
            no_earnings_decimal = None
        
        if soup.find("th", text="Population Density"):
            pod_header = soup.find("th", text="Population Density")
            pod = pod_header.find_next_sibling("td").text
            pod = pod.strip('$')
            pod = pod.replace(',', '')
            if pod != 'n/a':
                pod = int(pod)
            else:
                pod = None
        else:
            pod = None

        with open(f'{output_folder}/{file_name_without_extension}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['zipcode', 'Median income', 'Median home value', 'Less than High School Diploma', 'High School Graduate', 'Associate degree','Bachelor degree','Master degree', 'Professional school degree', 'Doctorate degree', 'Unemployment rate','Population Density'])
            writer.writerow([zip_code, median_income, median_home_value, percentages[0],percentages[1], percentages[2], percentages[3], percentages[4], percentages[5], percentages[6], no_earnings_decimal, pod])


    # 修改这个路径到包含HTML文件的文件夹
    folder_path = 'source3_html/'

    # 列出資料夾中的所有文件
    files = os.listdir(folder_path)
    #print(files)

    html_files = [f for f in files if f.endswith('.html')]
    #print(html_files)

    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        zip_code = html_file.split('/')[-1].split('_')[0]
        #print(file_path)
        with open(file_path, 'rb') as fin:
            soup = BeautifulSoup(fin.read(), 'html.parser')
            if soup.find("body"):
                parse_html_file(zip_code, soup, file_path)
                #soup = BeautifulSoup(fin.read(), 'html.parser')
                #print(soup)

