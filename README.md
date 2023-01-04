# Pianobaren

A thingie that reads rfid tags, starts mplayer playing music connected to that rfid tag, and manipulates the music in realtime so it sounds like and old cassette player.


To map rfid tags with a folder to play make a file called config.json and do something like this:

```json

 {
    "0014030686": "/Users/peppe/Music/Ripped/Soul/",
    "0009148262": "/Users/peppe/Music/Ripped/Hiphop/"
}
```

Take note, the rfid takes a second or two to be able to read a new tag, so don't spam it.

https://forum.clockworkpi.com/t/how-to-disable-wifi-power-save-to-prevent-disconnects/933
https://unix.stackexchange.com/questions/269661/how-to-turn-off-wireless-power-management-permanently
https://askubuntu.com/questions/1339765/replacing-pulseaudio-with-pipewire-in-ubuntu-20-04/1339897#1339897

Packages needed:

sudo apt-get purge needrestart

sudo apt-get install virtualenv virtualenvwrapper python3-rpi.gpio mplayer mpv
sudo apt-get install wireless-tools
sudo apt-get install pipewire-audio-client-libraries pulseaudio-utils pulseaudio alsa-utils pipewire-bin


git clone git@github.com:peppelorum/Pianobaren.git
cd Pianobaren; virtualenv .venv;

cd Pianobaren; source .venv/bin/activate


cat ../.asoundrc
#defaults.bluealsa.service "org.bluealsa"
#defaults.bluealsa.device "F3:84:2C:18:CC:13"
#defaults.bluealsa.profile "a2dp"
#defaults.bluealsa.delay 10000
#
defaults.pcm.card 1
defaults.ctl.card 0

