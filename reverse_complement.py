# Requires biopython
import argparse
from Bio import SeqIO

# Create an argument parser
parser = argparse.ArgumentParser(description='Reverse complement DNA sequences in a CSV file.')
parser.add_argument('input_file', type=str, help='Path to the input file')
parser.add_argument('column', type=str, help='Name of the column containing DNA sequences')
parser.add_argument('output_file', type=str, help='Path to the output file')
parser.add_argument('--delimiter', type=str, default=',', help='Delimiter used in the input file (default: ",")')
args = parser.parse_args()

input_file = args.input_file
column_name = args.column
output_file = args.output_file
delimiter = args.delimiter

# Read the file, assuming it has a header row
with open(input_file, 'r') as file:
    lines = file.readlines()

header = lines[0].strip().split(delimiter)  # Get the header names
column_index = header.index(column_name)  # Find the index of the specified column

# Add the new header for the reverse complemented column
header.append(f'{column_name}_revcomp')

# Process each row, reverse complementing the sequence in the specified column and adding it to the new column
for i in range(1, len(lines)):
    row = lines[i].strip().split(delimiter)

    # Reverse complement the DNA sequence using Biopython
    sequence = row[column_index]
    revcomp_sequence = str(Seq(sequence).reverse_complement())

    # Add the reverse complemented sequence to the new column
    row.append(revcomp_sequence)

    # Update the row in the lines array
    lines[i] = delimiter.join(row)

# Write the updated data back to the output file
with open(output_file, 'w') as file:
    file.writelines(lines)
