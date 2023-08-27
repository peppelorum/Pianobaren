# recordsong.py - record a song on Spotify with the help of Piezo

# Example usage:
#
# python3 recordsong.py spotify:track:21cp8L9Pei4AgysZVihjSv
# or
# python recordsong.py https://open.spotify.com/playlist/6GhGrpKtVEe4CFNEXvnEgL?si=dded0ffc75c542ac


import subprocess
import sys
import os
import time
import shutil
import eyed3
from urllib.request import urlopen
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_playlist_ids(username, playlist_id):
    r = sp.user_playlist_tracks(username, playlist_id)
    t = r['items']
    ids = []
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t:
        ids.append(s["track"]["id"])
    return ids


# Setup variables
piezoStorageLocation = '/Users/peppe/Music/Piezo/'
ripStorageLocation = '/Users/peppe/Music/Ripped/'
playlistId = sys.argv[1]
folder = sys.argv[2]

if 'https' in sys.argv[1]:
    playlistId = b = sys.argv[1].split('/')[-1].split('?')[0]


print('playlistId', playlistId)


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="b67053ce0a7d4990acac4d0c935b0776", client_secret="49626db34dbc4ed4836a270ca332f7c6"))

a = get_playlist_ids('peppelorum', playlistId)
for song in a:
    songId = 'spotify:track:' + song
    print('songId', song, songId)

    # # Tell Spotify to pause, tell Piezo to record, tell Spotify to play a specified song

    subprocess.Popen('osascript -e "tell application \\"Spotify\\" to pause"',
                     shell=True, stdout=subprocess.PIPE).stdout.read()
    time.sleep(.300)

    subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "play track \\"' +
                     songId + '\\"" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()
    time.sleep(.300)
    subprocess.Popen('osascript -e "tell application \\"Spotify\\" to pause"',
                     shell=True, stdout=subprocess.PIPE).stdout.read()
    time.sleep(.300)

    # Get the artist name, track name, album name and album artwork URL from Spotify
    artist = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artist" -e "end tell"',
                              shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
    track = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s name" -e "end tell"',
                             shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
    album = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s album" -e "end tell"',
                             shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
    artwork = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artwork url" -e "end tell"',
                               shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')

    songname = artist+" - "+track+".mp3"
    songpath = os.path.join(ripStorageLocation, folder, songname)

    print('songpath', songpath)

    if os.path.exists(songpath):
        print('Skipping: ' + songname)
        continue

    subprocess.Popen(
        'osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen('osascript -e "tell application \\"Spotify\\" to play"',
                     shell=True, stdout=subprocess.PIPE).stdout.read()
    time.sleep(1)

    # Download album artwork
    artworkData = urlopen(artwork).read()

    # Check every 500 milliseconds if Spotify has stopped playing
    while subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "player state" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read() == b"playing\n":
        time.sleep(.100)

    subprocess.Popen('osascript -e "tell application \\"Spotify\\" to pause"',
                     shell=True, stdout=subprocess.PIPE).stdout.read()
    time.sleep(.300)

    # Spotify has stopped playing, stop the recording in Piezo
    subprocess.Popen(
        'osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()

    time.sleep(.500)

    # Create directory for the playlist
    if not os.path.exists(os.path.join(ripStorageLocation, folder)):
        os.makedirs(os.path.join(ripStorageLocation, folder))

    # Move MP3 file from Piezo folder to the folder containing rips.
    for f in os.listdir(piezoStorageLocation):
        if f.endswith(".mp3"):
            shutil.move(piezoStorageLocation+f, songpath)

    # Set and/or update ID3 information
    musicFile = eyed3.load(songpath)
    # musicFile.tag.images.set(3, artworkData, "image/jpeg", playlistId)
    musicFile.tag.artist = artist
    musicFile.tag.album = album
    musicFile.tag.title = track

    musicFile.tag.save()


# Clear all previous recordings if they exist
# for f in os.listdir(piezoStorageLocation):
#     os.remove(os.path.join(piezoStorageLocation,f))
