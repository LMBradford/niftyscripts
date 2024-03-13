# Usage: python count_fastqreads_rough.py -o output.csv --prefix 'SRR'

import os
import glob
import subprocess
import pandas as pd
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Count reads in fastq files.')

# Add the arguments
parser.add_argument('-o','--OutputFile',
                    metavar='output_file',
                    type=str,
                    help='the name of the output file')
parser.add_argument('-p','--prefix', 
                    type=str, 
                    help='prefix pattern of the input files. Optional')                    

# Parse the arguments
args = parser.parse_args()

def count_fastq_reads(directory=None, output_file=args.OutputFile):
    # If no directory is specified, use the current working directory
    if directory is None:
        directory = os.getcwd()

    # Get all fastq.gz files matching a given pattern
    files = glob.glob(f'{args.prefix}*.fastq.gz')
    print(files)
    # List to store the results
    data = []

    # Count the number of reads in each file
    for file in files:
        cmd = f'gunzip -c {file} | wc -l'
        lines = int(subprocess.check_output(cmd, shell=True))
        reads = lines // 4
        samplename = os.path.basename(file).split('.')[0]
        data.append({'samplename': samplename, 'reads': reads})

    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    # Output the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    print(df)

# Usage
count_fastq_reads()