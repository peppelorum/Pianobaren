import os
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

with open('config.json', 'r') as f:
    playlists = json.load(f)

class ServerService(rpyc.Service):
    def on_connect(self, conn):
        self._conn = conn

    def exposed_loadtag(self, arg):
        playlist = playlists[arg]
        self.exposed_loadfile(playlist)


    def exposed_loadfile(self, arg):
        mp3_list = [i for i in os.listdir(arg) if i[-3:] == "mp3"]
        mp3_list = '\n'.join(mp3_list)

        playlist = f'{arg}playlist.txt'
        fp = open(playlist, "w")
        fp.write(mp3_list)
        fp.close()

        mp.loadlist(playlist)

        asyncio.run(display_date())

        # loop = asyncio.get_event_loop()
        # # Blocking call which returns when the display_date() coroutine is done
        # loop.run_until_complete(self.display_date(loop))
        # loop.close()



async def display_date():
    print('Hello ...')
    mp.command('speed_incr 0.1')
    print(mp.get_property('speed'))

    await asyncio.sleep(1)
    mp.command('speed_incr 0.1')
    await asyncio.sleep(1)
    print('... World!')

    print(mp.get_property('speed'))

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

#
        # mp.command("volume 50 1")

    finally:
        print('knas')
        # mp.command('quit')

    server.start()
    print('då')