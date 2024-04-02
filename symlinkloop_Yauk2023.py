import os
import sys
import argparse

#Usage: python3 symlinkloop_Yauk2023.py inputfile.txt -s _ -i 0 
# Requires an input file with the full path to the fastq files, one per line.

def create_symbolic_link(original_path, link_path):
    try:
        os.symlink(original_path, link_path)
        print(f"Created symbolic link: {link_path}")
    except FileExistsError:
        print(f"Symbolic link already exists: {link_path}")

# Create the parser
parser = argparse.ArgumentParser(description='Create symbolic links to fastq files.')

# Add the arguments
parser.add_argument('input_file', 
                    type=str, 
                    help='the input file containing the original file paths')
parser.add_argument('-s','--split_pattern', 
                    type=str, 
                    default='_',
                    help='pattern to split the file names on. Default is "_"',
                    required=True)
parser.add_argument('-i','--index', 
                    type=int, 
                    default=0,
                    help='index of the part to use as the sample name after splitting the file name. Default is 0')                    

# Parse the arguments
args = parser.parse_args()

def main():
    with open(args.input_file, 'r') as file:
        for line in file:
            original_path = line.strip()
            
            # Extracting relevant information from the filename
            filename = os.path.basename(original_path)
            parts = filename.split(args.split_pattern)
            sample_name = parts[args.index]
            new_filename = f"{sample_name}.fastq.gz"
            
            # Constructing the new symbolic link path
            link_path = os.path.join(os.getcwd(), filename)
            
            #Tests
            # print(original_path)
            # print(new_filename)

            #Create symbolic link
            create_symbolic_link(original_path, link_path)

if __name__ == "__main__":
    main()