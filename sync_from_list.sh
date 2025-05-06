#!/bin/bash

# Source directory containing all the directories to be synced
SOURCE_DIR="/mnt/nextseqData/Runs"

# Destination directory
DEST_DIR="/mnt/raw_data/genomicslab_inhouse/2025/"

# Read the directories from the file and loop through each one
while IFS= read -r dir; do
  echo "Syncing $SOURCE_DIR/$dir to $DEST_DIR"
  # rsync -arPn "$SOURCE_DIR/$dir" "$DEST_DIR" --exclude="*.jpg" # -n for dry run
  rsync -arP "$SOURCE_DIR/$dir" "$DEST_DIR" # uncomment this line to actually sync the files
done < dir_to_sync_to_new_netapp.txt