#!/bin/bash

# Update bashrc
echo "export TSVTOOL=$PWD" >> ~/.bashrc
source ~/.bashrc

# Install python3 requirements
python3 -m  pip install -r bin/python3/requirements.txt
