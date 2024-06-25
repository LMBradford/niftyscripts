import argparse
import pandas as pd
from Bio import Seq

# Usage: python reverse_complement.py input.csv sequence_column output.csv --delimiter tab --skip_before 1 --skip_after 2

# Create an argument parser
parser = argparse.ArgumentParser(description='Reverse complement DNA sequences in a CSV file.')
parser.add_argument('input_file', type=str, help='Path to the input file')
parser.add_argument('column', type=str, help='Name of the column containing DNA sequences')
parser.add_argument('output_file', type=str, help='Path to the output file')
parser.add_argument('--delimiter', type=str, default=',',
                    choices=[',', 'tab'], help='Delimiter used in the input file. Options: tab or ,')
parser.add_argument('--skip_before', type=int, default=0, help='Number of lines to skip before the table begins in input file'),
parser.add_argument('--skip_after', type=int, default=0, help='Number of lines to skip after the table ends in input file'),
args = parser.parse_args()

input_file = args.input_file
column_name = args.column
output_file = args.output_file

# Read the file into a pandas DataFrame
if args.delimiter == ",":
    df = pd.read_csv(input_file, skiprows=args.skip_before, skipfooter=args.skip_after)
if args.delimiter == "tab":
    df = pd.read_csv(input_file, sep="\t", skiprows=args.skip_before, skipfooter=args.skip_after)  

# Reverse complement the DNA sequences in the specified column
df[f'{column_name}_revcomp'] = df[column_name].apply(lambda seq: str(Seq.Seq(seq).reverse_complement()))

# Save the updated DataFrame to the output file
# With same delimiter as input
if args.delimiter == ",":
    df.to_csv(output_file, index=False)
if args.delimiter == "tab":
    df.to_csv(output_file, index=False, sep="\t")

print(f'Created {output_file}.')
