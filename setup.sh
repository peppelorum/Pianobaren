#!/bin/bash

python3 -m venv .venv &
source .venv/bin/activate &
pip3 install -r requirements.txt &

sudo systemctl stop server.service &
sudo cp services/server.service /etc/systemd/system/server.service &
sudo systemctl daemon-reload &
sudo systemctl start server.service &
sudo systemctl status server.service

sudo systemctl stop buttons.service &
sudo cp services/buttons.service /etc/systemd/system/buttons.service &
sudo systemctl daemon-reload &
sudo systemctl start buttons.service &
sudo systemctl status buttons.service


