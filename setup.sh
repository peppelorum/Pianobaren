#!/bin/bash

python3 -m venv .venv &
source .venv/bin/activate &
pip3 install -r requirements.txt &
systemctl stop bar.service &
cp bar.service /etc/systemd/system/bar.service &
systemctl daemon-reload &
systemctl start bar.service &
sudo systemctl status bar.service
