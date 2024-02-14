import os
import glob
import subprocess
import pandas as pd

def count_fastq_reads(directory=None, output_file='readcount_rough.csv'):
    # If no directory is specified, use the current working directory
    if directory is None:
        directory = os.getcwd()

    # Get all fastq.gz files in the directory
    files = glob.glob('*.fastq.gz')

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
count_fastq_reads('readcount_rough.csv')