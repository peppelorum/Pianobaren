#!/bin/bash

python3 -m venv .venv &
source .venv/bin/activate &
pip3 install -r requirements.txt &
sudo systemctl stop bar.service &
sudo cp bar.service /etc/systemd/system/bar.service &
sudo systemctl daemon-reload &
sudo systemctl start bar.service &
sudo systemctl status bar.service
