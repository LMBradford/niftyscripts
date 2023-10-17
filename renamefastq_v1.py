#This script isn't very fancy or general
#Just edit glob and loop variables
##as needed to match your files du jour

from os import rename
from glob import glob

FNAMES = glob('*_S*_R*_001.fastq.gz')

print(FNAMES)

for fname in FNAMES:
  sample = fname.split("_")[0]
#  prefix = fname.split("_")[1]
#  fwdrev = fname.split("_")[5]
  
  newname = f"{sample}.fastq.gz"
  
  rename(fname, newname)
  
  print(f"{fname} has been renamed to {newname}")