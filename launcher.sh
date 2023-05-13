#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-virtualenv
virtualenv venv -p python3
source venv/bin/activate
export TOKEN=$1
pip install -r requirements.txt
chmod +x bot.py
python3 bot.py