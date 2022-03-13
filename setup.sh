

pip3 install -r requirements.txt

systemctl stop bar.service
cp bar.service /etc/systemd/system/bar.service
systemctl daemon-reload
systemctl start bar.service
sudo systemctl status bar.service
