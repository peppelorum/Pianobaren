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
        playlist = playlists[arg]
        self.exposed_loadfile(playlist)

    def exposed_pitch(self, arg):
        global pitchActive
        pitchActive = arg
        # print(pitchActive)

    def exposed_loadfile(self, arg):
        mp3_list = [i for i in os.listdir(arg) if i[-3:] == "mp3"]
        mp3_list = '\n'.join(mp3_list)

        playlist = f'{arg}playlist.txt'
        fp = open(playlist, "w")
        fp.write(mp3_list)
        fp.close()

        mp.loadlist(playlist)

        pitch()


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
        print(mp.get_property('speed'))
        print('.')
        time.sleep(1)
        # await asyncio.sleep(0.01)


if __name__ == "__main__":
    server = ThreadedServer(ServerService, port = 12345)

    MPlayer.populate()
    try:
        mp = MPlayer()
        # mp.loadlist('/Users/peppe/Music/Ripped/Soul/playlist.txt')


        # while True:
        #     mp.command('speed_incr 0.1')
        #     time.sleep(1)
        #     print('.')


        mp.af_add('scaletempo=scale=1.0:speed=pitch');

#
        # mp.command("volume 50 1")

    finally:
        print('knas')
        # mp.command('quit')

    server.start()
    print('då')