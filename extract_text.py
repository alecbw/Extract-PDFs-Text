import sys
import os
import argparse
import logging
import csv

try:
    import pdfplumber
    from langdetect import detect

except ImportError:
    sys.exit("~ Make sure you install pdfplumber and langdetect. Run `pip install pdfplumber langdetect` and try this again ~")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

########################################################################################


argparser = argparse.ArgumentParser()
argparser.add_argument('-file', nargs='?', default="all", help="The name of your file")
argparser.add_argument('-output', nargs='?', default="csv", help="What output type you want (txt or csv). Default behavior is csv")

args = argparser.parse_args()


########################################################################################

"""
A couple friendly notes:
Writes to CSV may have formatting problems where newlines cause what should be written
to one cell to explode across many rows and columns. Try to use .txt outputs instead.
txt will write 1 to 1 to inputs; csv is many to 1 output.

Do also nte:
    CSV cell character limit is 131072
    Google Sheet's is 50000
"""

def ingest_pdf(filename, output):
    if filename == "all":
        output_lod = []
        list_of_files = [f for f in os.listdir('.') if os.path.isfile(f) and ".pdf" in f]
        logging.info(f"{len(list_of_files)} PDF files were found")
        logging.info(list_of_files)
        for file in list_of_files:
            output_lod.append(extract_text_from_pdf(file))
    else:
        output_lod = [extract_text_from_pdf(filename)]

    logging.info(len(output_lod))

    if output == "txt":
        for row in output_lod:
            with open(f"Processed PDF Text {row['File'].replace('.pdf', '')}.txt", "w") as text_file:
                text_file.write(row["Text"])

    elif output == "csv":
        with open(f"Processed PDF Text {filename.replace('.pdf', '')}.csv", 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(output_lod)

    logging.info('written')

def extract_text_from_pdf(filename):
    output_dict = {"File": filename, "Text": ""}
    with pdfplumber.open(os.getcwd() + "/" + filename) as pdf:
        for n, page in enumerate(pdf.pages):
            if page.extract_text():
                output_dict["Text"] += page.extract_text().replace("\n", "").replace("\r", "")
            if n % 10 == 0:
                logging.info(f"Now on page {n}")

    output_dict["Language"] = detect(output_dict["Text"])
    logging.info('finished')
    return output_dict

ingest_pdf(args.file, args.output)
