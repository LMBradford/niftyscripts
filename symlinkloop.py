import os
import sys
import argparse

#Usage: python3 symlinkloop.py inputfile.txt --split_pattern _S --index 0 
# Requires an input file with the full path to the fastq files, one per line.
# Use --test to see anticipated output without actually running
# Use the splitter (--split-pattern and --index) to keep only the desired parts of the file name.
## Usual use is --split-pattern _S and -i 0. This removes the ex. "_S1_R1_001" part which is generally unwanted
## Problems arise if researcher used _S in sample names. Tell them not to do that.

def create_symbolic_link(original_path, link_path):
    try:
        os.symlink(original_path, link_path)
        print(f"Created symbolic link: {link_path}")
    except FileExistsError:
        print(f"Symbolic link already exists: {link_path}")

parser = argparse.ArgumentParser(description='Create symbolic links to fastq files.')

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
parser.add_argument('--test',
                    required=False,
                    action='store_true',
                    help='Test mode: print the original path and the new filename, but do not create the symbolic links')                    

# Parse the arguments
args = parser.parse_args()

def main():
    with open(args.input_file, 'r') as file:
        for line in file:
            original_path = line.strip()
            
            # Extract relevant information from the filename
            filename = os.path.basename(original_path)
            parts = filename.split(args.split_pattern)
            sample_name = parts[args.index]
            new_filename = f"{sample_name}.fastq.gz"
            
            # Construct the new symbolic link path
            link_path = os.path.join(os.getcwd(), new_filename)
            
            # Tests
            if args.test:
                print(f"{new_filename} linked to {original_path}")
            else:
                # Actually create symbolic link
                create_symbolic_link(original_path, link_path)

if __name__ == "__main__":
    main()