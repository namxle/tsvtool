#!/bin/bash

mkdir -p ~/.venv

python3 -m venv ~/.venv

source ~/.venv/bin/activate

python3 -m pip install -r python3/requirements.txt