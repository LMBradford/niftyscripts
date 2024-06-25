# Concatenate files with different names in the same directory
# Use in the directory containing the files to be combined

# Usage:    python combinefastqFC_diffnames.py -o outputdir -s '_FC'        


import os
import glob
import argparse

def concatenate_files(input_directory=None, output_directory=None):
    # If no input directory is specified, use the current working directory
    if input_directory is None:
        input_directory = os.getcwd()

    # If no output directory is specified, use the input directory
    if output_directory is None:
        output_directory = input_directory

    # Get all fastq.gz files in the input directory
    files = glob.glob('*.fastq.gz')

    # Group files by pattern before FC
    pattern_dict = {}
    for file in files:
        # Extract pattern before FC from filename
        pattern, _ = os.path.basename(file).split(args.split_pattern, 1)
        if pattern not in pattern_dict:
            pattern_dict[pattern] = []
        pattern_dict[pattern].append(file)

    # Concatenate files in each group
    for pattern, file_group in pattern_dict.items():
        output_file = os.path.join(output_directory, f'{pattern}.fastq.gz')
        # Check if output file already exists
        if os.path.exists(output_file):
            print(f"Output file {output_file} already exists. Skipping...")
            continue

        print(f"Files {', '.join(file_group)} were concatenated to {output_file}")
        with open(output_file, 'wb') as outfile:
            for file in file_group:
                with open(file, 'rb') as infile:
                    outfile.write(infile.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate FASTQ files.')
    parser.add_argument('-o', '--output', help='Output directory', required=True)
    parser.add_argument('-s','--split_pattern', 
                    type=str,
                    help='pattern to split the file names on. Files with identical names before this pattern will be concatenated.',
                    required=True)
    args = parser.parse_args()

    concatenate_files(output_directory=args.output)


