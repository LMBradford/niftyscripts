
# Usage: Rscript revcomp_i5_indices.R test_file seqtype
# Description: This script reads a test file and checks the i5 index against a set of forward and reverse complement indices.
# It then corrects the index if it is a reverse complement of the index for the sequencer type specified.
# Example: Rscript revcomp_i5_indices.R test_file.csv nextseq500
# Options for seqtype: nextseq500, nextseq2000

# Suppress package startup messages
suppressPackageStartupMessages(library(dplyr))

# Get the test file name from the command line arguments
args <- commandArgs(trailingOnly = TRUE)
test_file <- args[1]

seqtype <- args[2]

# Put args[2] in all lower case
seqtype <- tolower(seqtype)

# Read the illumina_i5_indices.txt file
illumina_df <- read.delim("illumina_i5_indices.txt", header = TRUE, stringsAsFactors = FALSE)

# Read the test CSV file as lines to find the row with "Sample_ID"
lines <- readLines(test_file)
start_row <- which(grepl("^Sample_ID", lines))

# Now read the file from the found row, assuming "Sample_ID" is the header
test_df <- read.csv(test_file, skip = start_row - 1, header = TRUE)

# Function to correct i5 indices
correct_i5_index <- function(index, seqtype, illumina_df) {
  if (seqtype == "nextseq500") {
    if (index %in% illumina_df$i5_revcomp_NextSeq500) {
      return(index)
    } else if (index %in% illumina_df$i5_fwd_NextSeq2000) {
      return(illumina_df$i5_revcomp_NextSeq500[illumina_df$i5_fwd_NextSeq2000 == index])
    }
  } else if (seqtype == "nextseq2000") {
    if (index %in% illumina_df$i5_fwd_NextSeq2000) {
      return(index)
    } else if (index %in% illumina_df$i5_revcomp_NextSeq500) {
      return(illumina_df$i5_fwd_NextSeq2000[illumina_df$i5_revcomp_NextSeq500 == index])
    }
  }
  return(NA) # Return NA if no match found
}

# Apply the function to test_df$index2
test_df$corrected_i5 <- sapply(test_df$index2, correct_i5_index, seqtype, illumina_df)

# Replace index2 with the corrected index
new_df <- test_df
new_df$index2 <- new_df$corrected_i5
new_df$corrected_i5 <- NULL

# Get the header lines from the original file
header_lines <- lines[1:(start_row - 1)]

# Write the corrected file with header lines and the new df
file_name <- sub("\\.[^.]*$", "", test_file)

writeLines(header_lines, paste0(file_name, "_i5corrected.csv"))
write.table(new_df, file = paste0(file_name, "_i5corrected.csv"), row.names = FALSE, col.names = TRUE, sep = ",", append = TRUE, quote = FALSE)
