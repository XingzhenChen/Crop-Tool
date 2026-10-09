#!/bin/bash
source "$(dirname "$0")/venv/bin/activate"

for i in ./*.pdf
do
    python3 ./crop.py ${i}

done
