import os
import random
from signal import pause
import time
from traceback import print_list
import rpyc
from mplayer import MPlayer
from rpyc.utils.server import ThreadedServer # or ForkingServer
import subprocess
import asyncio
import datetime
import json

pitchActive = True
pitchUp = True

with open('config.json', 'r') as f:
    playlists = json.load(f)


class ServerService(rpyc.Service):
    def on_connect(self, conn):
        self._conn = conn

    def exposed_loadtag(self, arg):
        folder = playlists[arg]
        makeplaylist(arg)
        playlist = f'{folder}playlist.txt'
        mp.loadlist(playlist)

        pitch()

    def exposed_pitch(self, arg):
        global pitchActive
        pitchActive = arg

    def exposed_unload(self):
        print('unload')
        stop()


def makeplaylist(tag):
    folder = playlists[tag]
    mp3_list = [i for i in os.listdir(folder) if i[-3:] == "mp3" or i[-3:] == "wav" or i[-3:] == "m4a"]
    mp3_list = '\n'.join(mp3_list)

    playlist = f'{folder}playlist.txt'
    fp = open(playlist, "w")
    fp.write(mp3_list)
    fp.close()

    return playlist


def stop():
    print(1)
    mp.stop()
    noise.stop()

    playlistlocation = makeplaylist('unload')
    noise.loadlist(playlistlocation)
    noise.play()


def pitch():
    global pitchUp, pitchActive
    print('Hello ...')
    i = 0
    limitlower = 0.8
    limitupper = 1.2
    speed = 1.0
    while pitchActive:
        if pitchUp:
            newspeed = speed + random.uniform(0.05, 0.1)
        else:
            newspeed = speed + random.uniform(-0.1, -0.05)

        if newspeed < limitlower:
            pitchUp = True
            limitupper = random.uniform(1.1, 1.4)
        elif newspeed > limitupper:
            pitchUp = False
            limitlower = random.uniform(0.7, 0.9)
        else:
            speed = newspeed

        mp.command(f'speed_set {speed}')
        # print(mp.get_property('speed'))
        print('.')
        # time.sleep(1)
        # await asyncio.sleep(0.01)


if __name__ == "__main__":
    server = ThreadedServer(ServerService, port = 12345)

    MPlayer.populate()
    try:
        mp = MPlayer()
        noise = MPlayer()

        playlistlocation = makeplaylist('noise')
        noise.loadlist(playlistlocation)

        mp.af_add('scaletempo=scale=1.0:speed=pitch');

        # time.sleep(10)
        # stop()

    finally:
        print('knas')
        # mp.command('quit')

    server.start()
    print('då')