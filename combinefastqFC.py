# Fastq files for the same sample across different seq runs
# Same name per sample, but each run in different dir
# Concatenate all fastq for a sample together

# Usage: python combinefastqFC.py -i /path/to/dir1/ /path/to/dir2/ -o /path/to/outputdir/ -e fastq.gz
# Use --test flag to see what will be done without actually doing it

import os
from glob import glob
from argparse import ArgumentParser
from pathlib import Path

# Arguments
parser = ArgumentParser(
	description=
	'''
	Goal: Concatenate fastq.gz files that have the same name but are in different directory (i.e. same sample, multiple sequencing runs).
	Files must be all have the same extension (specify in command).
	Give full directory paths. Relative paths will probably break things (not tested).
	Output directory MUST be different from input directory or you will overwrite original files and be in REAL trouble.
	''')

parser.add_argument('-i', '--inputdirs', nargs='+', default=[],
					help='full paths to input directories, space separated. Include final / !')
parser.add_argument('-o', '--outdir',
					help='full path to output directory. Include final / !')
parser.add_argument('-e', '--extension',
					help='specify fastq.gz or fq.gz. Must be gzipped!')
parser.add_argument('-t', '--test', action='store_true')
args = parser.parse_args()

# Make output directory if not preexisting
Path(args.outdir).mkdir(parents=True, exist_ok=True)

# Add slashes to end of dirs if not already there
for i in range(len(args.inputdirs)):
	if not args.inputdirs[i].endswith('/'):
		args.inputdirs[i] = args.inputdirs[i] + '/'

if not args.outdir.endswith('/'):
	args.outdir = args.outdir + '/'

# Find sample names
#Presumes all samples are in the first directory on the list!
SAMPLEPATHS = glob(f'{args.inputdirs[0]}*.{args.extension}')

# Get sample names without path
SAMPLEFILES = []
for sampath in SAMPLEPATHS:
	fnameext = os.path.basename(sampath)
	SAMPLEFILES.append(fnameext)

# Link all directories with file names
filepaths = {}
for f in SAMPLEFILES:
	for d in args.inputdirs:
		if f not in filepaths:
			filepaths[f] = []
		filepaths[f].append(d)
 
# Concatenate files into output directory
for f in filepaths:
	x = []
	for i in filepaths[f]:
		x.append(f'{i}{f}')
	tocat = ' '.join(x)

	samplename = f.split('.')[0] # Take sample name before first period
	cmd = f'cat {tocat} > {args.outdir}{samplename}.{args.extension}'

	# Test mode
	if args.test:
		print(f'Will create {args.outdir}{samplename}.{args.extension} with command: {cmd}')

	if not args.test:
		os.system(cmd)
		print(f'Created {args.outdir}{samplename}.{args.extension}')

# print(cmd) # For testing