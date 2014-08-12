#!/bin/bash
# Run this automated testing program

mkdir -p log

sh import-sql.sh

cd ../project-python-unittest/python-unittest/
python main.py


