#This script isn't very fancy or general
#Just edit glob and loop variables
##as needed to match your files du jour

from os import rename
from glob import glob

FNAMES = glob('*_S*_R*_001.fastq.gz')

print(FNAMES)

for fname in FNAMES:
#  sample1 = fname.split("_")[0]
  sections = fname.split("_")[:4]
  #Need an underscore between each section 

  sample = "_".join(sections)

#  prefix = fname.split("_")[1]
#  fwdrev = fname.split("_")[5]
  
  newname = f"{sample}.fastq.gz"
  
  rename(fname, newname)
  
  print(f"{fname} has been renamed to {newname}")