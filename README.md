# Pianobaren

A thingie that reads rfid tags, starts mplayer playing music connected to that rfid tag, and manipulates the music in realtime so it sounds like and old cassette player.


To map rfid tags with a folder to play make a file called config.json and do something like this:

```json

 {
    "0014030686": "/Users/peppe/Music/Ripped/Soul/",
    "0009148262": "/Users/peppe/Music/Ripped/Hiphop/"
}
```