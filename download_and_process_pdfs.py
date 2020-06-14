
import pandas as pd

import logging
import csv
import os

import pdfplumber
from langdetect import detect
logger = logging.getLogger()
logger.setLevel(logging.INFO)

######################

# Note: CSV cell character limit is 131072
# Google Sheet's is 50000
# url = "http://www.oshc.org.hk/oshc_data/files/leaflets/2016/Household_Flyer_Eng.pdf"

def ingest_pdf(filename, output):
    if filename == "all":
        output_lod = []
        list_of_files = [f for f in os.listdir('.') if os.path.isfile(f) and ".pdf" in f]
        print(f"{len(list_of_files)} PDF files were found")
        print(list_of_files)
        for file in list_of_files:
            output_lod.append(extract_text_from_pdf(file))
    else:
        output_lod = [extract_text_from_pdf(filename)]

    print(len(output_lod))

    if output == "txt":
        for row in output_lod:
            with open(f"Processed PDF Text {row['File'].replace('.pdf', '')}.txt", "w") as text_file:
                text_file.write(row["Text"])

    elif output == "csv":
        with open(f"Processed PDF Text {filename.replace('.pdf', '')}.csv", 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(output_lod)

    print('written')

def extract_text_from_pdf(filename):
    output_dict = {"File": filename, "Text": ""}
    with pdfplumber.open(os.getcwd() + "/" + filename) as pdf:
        for n, page in enumerate(pdf.pages):
      # first_page = pdf.pages[0]
      # print(first_page.chars[0])
            if page.extract_text():
                output_dict["Text"] += page.extract_text().replace("\n", "").replace("\r", "")
            if n % 10 == 0:
                print(f"Now on page {n}")

    output_dict["Language"] = detect(output_dict["Text"])
    print('finished')
    return output_dict

ingest_pdf("all", "txt")
