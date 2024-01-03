import os
import sys

def create_symbolic_link(original_path, link_path):
    try:
        os.symlink(original_path, link_path)
        print(f"Created symbolic link: {link_path}")
    except FileExistsError:
        print(f"Symbolic link already exists: {link_path}")

def main(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            original_path = line.strip()
            
            # Extracting relevant information from the filename
            filename = os.path.basename(original_path)
            parts = filename.split('_')
            sample_name = parts[-4]
            pool_name = parts[-5]
            new_filename = f"{sample_name}_{pool_name}.fastq.gz"
            
            # Constructing the new symbolic link path
            link_path = os.path.join(os.getcwd(), new_filename)

            #Tests
            # print(original_path)
            # print(new_filename)
            
            # Creating symbolic link
            create_symbolic_link(original_path, link_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py inputfile.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)