#!/bin/bash

# Create the directory structure
mkdir -p ./model/test

# Change to the directory
cd ./model/test

# Download the required files
wget "https://zenodo.org/records/10041747/files/L3_Top_Segmentation_Model_Weight.hdf5"
wget "https://zenodo.org/records/10041747/files/L3_Top_Selection_Model_Weight.h5"

echo "Download complete."
