# NOTE: probably need to add skiprows to the read_csv line. Add an argument for it?
import argparse
import pandas as pd
from Bio import Seq

# Create an argument parser
parser = argparse.ArgumentParser(description='Reverse complement DNA sequences in a CSV file.')
parser.add_argument('input_file', type=str, help='Path to the input file')
parser.add_argument('column', type=str, help='Name of the column containing DNA sequences')
parser.add_argument('output_file', type=str, help='Path to the output file')
parser.add_argument('--delimiter', type=str, default=',',
                    choices=[',', 'tab'], help='Delimiter used in the input file. Options: tab or ,')
args = parser.parse_args()

input_file = args.input_file
column_name = args.column
output_file = args.output_file

# Read the file into a pandas DataFrame
if args.delimiter == ",":
    df = pd.read_csv(input_file)
if args.delimiter == "tab":
    df = pd.read_csv(input_file, sep="\t")  

# Reverse complement the DNA sequences in the specified column
df[f'{column_name}_revcomp'] = df[column_name].apply(lambda seq: str(Seq.Seq(seq).reverse_complement()))

# Save the updated DataFrame to the output file
# With same delimiter as input
if args.delimiter == ",":
    df.to_csv(output_file, index=False)
if args.delimiter == "tab":
    df.to_csv(output_file, index=False, sep="\t")