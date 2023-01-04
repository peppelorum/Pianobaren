import os
import random
from signal import pause
import time
from traceback import print_list
import rpyc

import mpv

from rpyc.utils.server import ThreadedServer  # or ForkingServer
import subprocess
import asyncio
import datetime
import json
import random

pitchActive = 0
pitchUp = True
playlist = ''
noiseplaylist = ''

with open('config.json', 'r') as f:
    playlists = json.load(f)


class ServerService(rpyc.Service):
    def on_connect(self, conn):
        self._conn = conn

    def exposed_loadtag(self, arg):
        global playlist
        folder = playlists[arg]
        playlist = makeplaylist(arg)
        print(arg)
        # playlist = f'{folder}playlist.txt'
        # mp.loadlist(playlist)
        # mp.stop()

        # pitch()

    # def exposed_pitch(self, arg):
    #     global pitchActive
    #     pitchActive = arg

    def exposed_unload(self):
        print('unload')
        stop()
        unload()

    def exposed_stop(self):
        print('stop')
        mp.command('')
        stop()

    def exposed_play(self):
        play()

    def exposed_ff(self):
        ff()

    def exposed_pitch(self):
        print('pitch')
        pitchToggle()

    def exposed_nest(self):
        print('nest')
        nest()

        # lsof -p $(pidof -s mplayer) 2>/dev/null | grep -E "[0-9]+r.*REG" | grep -oE "[^/]+$"


def makeplaylist(tag):
    folder = playlists[tag]
    mp3_list = [i for i in os.listdir(
        folder) if i[-3:] == "mp3" or i[-3:] == "wav" or i[-3:] == "m4a" or i[0] != "."]
    random.shuffle(mp3_list)
    mp3_list = '\n'.join(mp3_list)

    playlist = f'{folder}playlist.txt'
    fp = open(playlist, "w")
    fp.write(mp3_list)
    fp.close()

    return playlist


def unload():
    print('unload cassette')


def play():
    print('play')
    # noise.loadlist(noiseplaylist)
    # mpv.
    mpv.loadlist(playlist)


def ff():
    # print('ff')
    # mp.command('speed_set 100')
    print('hej')
    # print(mp.get_property('speed'))


def nest():
    pass
    # mp.command('pt_step 1')


def stop():
    mp.stop()
    noise.stop()

    pitchActive = 0

    # playlistlocation = makeplaylist('unload')
    # noise.loadlist(playlistlocation)
    # noise.play()


def pitchToggle():
    global pitchActive

    if pitchActive == 3:
        pitchActive = 0
    else:
        pitchActive += 1

    print(pitchActive)
    pitch()


def pitch():
    global pitchUp, pitchActive
    print('Pitch start')
    i = 0
    speed = 1.0

    originalPitchValue = pitchActive

    if pitchActive == 1:
        limitlower = 0.9
        limitupper = 1.1
    elif pitchActive == 2:
        limitlower = 0.8
        limitupper = 1.2
    elif pitchActive == 3:
        limitlower = 0.6
        limitupper = 1.4
    else:
        pass
        # mp.command(f'speed_set {speed}')

    while pitchActive != 0:
        if originalPitchValue != pitchActive:
            return

        if pitchUp:
            newspeed = speed + random.uniform(0.05, 0.1)
        else:
            newspeed = speed + random.uniform(-0.1, -0.05)

        if newspeed < limitlower:
            pitchUp = True
            speed = limitlower
        elif newspeed > limitupper:
            pitchUp = False
            speed = limitupper
        else:
            speed = newspeed

        # print('asd')
        mp.af = 'rubberband=transients=smooth:pitch=quality:window=short'
        # mp.af = 'scaletempo=stride=16:overlap=.68:search=10'
        mp.speed = speed
        # print('hejsan')
        # mpv.meta
        # mpv.af_command('')
        # mp.command(f'speed_set {speed}')
        # print(mp. get_property('speed'))
        print(pitchActive, speed)
        time.sleep(0.5)
        # await asyncio.sleep(0.01)


if __name__ == "__main__":
    server = ThreadedServer(ServerService, port=12345)

    try:

        mp = mpv.MPV(input_ipc_server='/tmp/mpvsocket', audio_display='no')
        noise = mpv.MPV(input_ipc_server='/tmp/mpvnoisesocket',
                        audio_display='no')

        # mpv.p

        # mp = MPlayer()
        # noise = MPlayer()

        # mp.loadlist('/Users/peppe/Music/Ripped/Hiphop/playlist.txt')

        # mpv.command(play='backward')
        # mpv.play()

        # noiseplaylist = makeplaylist('noise')
        # print(noiseplaylist)
        # noise.command('pausing loadlist {}'.format(playlistlocation))
        # noise.loadlist(noiseplaylist)
        # noise.stop()

        # mp.af_add('scaletempo2=max-speed=16')
        # mp.af_add('scaletempo=scale=1.0:speed=pitch');

        # time.sleep(10)
        # stop()

    finally:
        print('knas')
        # mp.command('quit')

    server.start()
    print('då')
