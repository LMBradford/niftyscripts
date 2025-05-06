import json
import csv
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Convert json file to csv file')

parser.add_argument('-i','--input_json',
                    type=str,
                    help='JSON-formatted input file')
parser.add_argument('-o', '--output_csv',
                    type=str,
                    help='Name of output csv file')

args = parser.parse_args()

# Use your input and output filenames here
json_file = args.input_json
csv_file = args.output_csv

with open(json_file) as f:
    data = json.load(f)["data"]

with open(csv_file, "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)