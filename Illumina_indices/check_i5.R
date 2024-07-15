# Description: This script reads a test file and checks the i5 index against a set of forward and reverse complement indices.
# Usage: Rscript check_i5.R test_file.csv

# Suppress package startup messages
suppressPackageStartupMessages(library(dplyr))

# Get the test file name from the command line arguments
args <- commandArgs(trailingOnly = TRUE)
test_file <- args[1]

# Read the illumina_i5_indices.txt file
illumina_df <- read.delim("illumina_i5_indices.txt", header = TRUE, stringsAsFactors = FALSE)

# Read the test CSV file
# Read the file as lines to find the row with "Sample_ID"
lines <- readLines(test_file)
start_row <- which(grepl("^Sample_ID", lines))

# Now read the file from the found row, assuming "Sample_ID" is the header
test_df <- read.csv(test_file, skip = start_row - 1, header = TRUE)


# Check for matches and record the type of match
test_df$match_type <- sapply(test_df$index2, function(index) {
	if(index %in% illumina_df$i5_fwd_NextSeq2000) {
		return("i5_fwd_for_NextSeq2000")
	} else if(index %in% illumina_df$i5_revcomp_NextSeq500) {
		return("i5_revcomp_for_NextSeq500")
	} else {
		return("No Match")
	}
})

# Summarize the match types made
result <- test_df %>%
	group_by(match_type) %>%
	summarize(count = n())

# Print message: 
cat("Samples properly set up for demultiplexing on NextSeq2000: ", result$count[result$match_type == "i5_fwd_for_NextSeq2000"], "\n")
cat("Samples properly set up for demultiplexing on NextSeq500: ", result$count[result$match_type == "i5_revcomp_for_NextSeq500"], "\n")
cat("Samples not matching known indices:", result$count[result$match_type == "No Match"], "\n")
