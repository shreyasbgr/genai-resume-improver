#!/bin/bash

# Update package list and install poppler-utils
sudo apt-get update
sudo apt-get install -y poppler-utils

# Verify Poppler installation
if command -v pdfinfo &> /dev/null
then
    echo "Poppler is installed and in the PATH"
else
    echo "Poppler is not in the PATH"
fi