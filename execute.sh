#!bin/bash

sh lint.sh

# install dependencies
pip3 install -r requirements.txt

#execute 
python3 ./main.py