#!/bin/bash

python3 -m venv .venv &
source .venv/bin/activate &
pip3 install -r requirements.txt &
sudo systemctl stop buttons.service &
sudo cp services/buttons.service /etc/systemd/system/buttons.service &
sudo systemctl daemon-reload &
sudo systemctl start buttons.service &
sudo systemctl status buttons.service
