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
import pickle

pitchActive = 0
pitchUp = True
playlist = 0
noiseplaylist = ''


# def my_log(loglevel, component, message):
#     loglevel = str(loglevel)
#     component = str(component)
#     message = str(message)
#     print('[{}] {}: {}'.format(loglevel, component, message))


# def my_log(loglevel, component, message):
#     print('[{}] {}: {}'.format(loglevel, component, message))

last_save_time = 0
pl_id: int = 0
song_id: int = None


mp = mpv.MPV(input_ipc_server='/tmp/mpvsocket',
             audio_display='no')
noise = mpv.MPV(input_ipc_server='/tmp/mpvnoisesocket',
                audio_display='no')


# def event_handler(event):
#     print(event)
#     if event.event_id == mpv.MpvEventID.PROPERTY_CHANGE:
#         prop_event = event.data
#         print(f'Property {prop_event.name} changed to {prop_event.data}')
#     # if event.event_id in [mpv.Events.end_file, mpv.Events.shutdown]:
#     #     with open(f'mpv_state_{playlist}.pkl', 'rb') as f:
#     #         pickle.dump((mp.filename, mp.time_pos), f)


# mp.register_event_callback(event_handler)

# # Load previous song and time if exists
# try:
#     with open('mpv_state.pkl', 'rb') as f:
#         filename, time_pos = pickle.load(f)
# except FileNotFoundError:
#     filename, time_pos = None, None


# # If there was a previous song and time, try to resume
# if filename is not None and time_pos is not None:
#     mp.wait_until_playing()
#     # Cycle through playlist to find the song
#     for i, item in enumerate(mp.playlist):
#         if item['filename'] == filename:
#             mp.playlist_pos = i
#             mp.wait_until_playing()
#             mp.time_pos = time_pos
#             break


def load_playlist_state():
    global pl_id, song_id
    print('asdasd')
    try:
        with open(f'mpv_state_{pl_id}.pkl', 'rb') as f:
            song_id, time_pos = pickle.load(f)
            print('load', song_id, time_pos)
    except FileNotFoundError:
        song_id, time_pos = None, None

    print(pl_id, song_id, time_pos)
    return song_id, time_pos


def save_playlist_state(time_pos):
    global pl_id, song_id, last_save_time

    current_time = time.time()
    # print(current_time, last_save_time, current_time - last_save_time)
    if current_time - last_save_time > 10 and song_id != None:
        last_save_time = current_time
        print('save', pl_id, song_id, time_pos)
        with open(f'mpv_state_{pl_id}.pkl', 'wb') as f:
            pickle.dump((song_id - 1, time_pos), f)


@mp.event_callback('start-file')
# @mp.event_callback('shutdown')
def start_file(event):
    global song_id
    # if song_id != None:
    # print('*****************', dir(event.data))
    song_id = event.data.playlist_entry_id
    print(event.data.playlist_entry_id)


# @mp.property_observer('time-pos')
# def time_observer(_name, value):
#     # Here, _value is either None if nothing is playing or a float containing
#     # fractional seconds since the beginning of the file.
#     print('time-pos', value)
#     if value != None:
#         # print('Now playing at {:.2f}s'.format(value))
#         save_playlist_state(value)
# # mp.register_event_callback('start-file', save_state)
# # mp.register_event_callback('shutdown', save_state)

# # mp.quit()


with open('config.json', 'r') as f:
    playlists = json.load(f)


class ServerService(rpyc.Service):
    def on_connect(self, conn):
        self._conn = conn

    def exposed_loadtag(self, arg):
        print('loadtag')
        global playlist, pl_id
        pl_id = arg
        folder = playlists[arg]
        playlist = makeplaylist(arg)
        print(arg)

        restoresongandpos()
        # playlist = f'{folder}playlist.txt'
        # mp.loadlist(playlist)
        # mp.stop()

        # pitch()

    # def exposed_pitch(self, arg):
    #     global pitchActive
    #     pitchActive = arg

    def exposed_unload(self):
        global song_id
        print('unload')
        print(mp.playlist_pos, song_id)
        save_playlist_state(mp.time_pos)
        song_id = None
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


def makeplaylist(tag):
    folder = playlists[tag]
    mp3_list = [i for i in os.listdir(
        folder) if i[-3:] == "mp3" or i[-3:] == "wav" or i[-3:] == "m4a" or i[0] != "."]
    # random.shuffle(mp3_list)
    mp3_list = '\n'.join(mp3_list)

    playlist = f'{folder}playlist.txt'
    fp = open(playlist, "w")
    fp.write(mp3_list)
    fp.close()

    return playlist


def unload():
    print('unload cassette')


def restoresongandpos():
    global playlist, song_id
    # Load previous song and time if exists
    index, time_pos = load_playlist_state()
    print('restoresongandpos', index, time_pos)
    # Load playlist
    # mp.wait_until_playing()
    mp.loadlist(playlist)  # replace with your actual playlist

    if index is not None and time_pos is not None:
        song_id = index
        print('resume', index, time_pos)
        mp.playlist_pos = index
        # mp.wait_until_playing()

        # Wait a bit to ensure the track is loaded
        # You might want to optimize this with an event listener instead of sleep

        time.sleep(0.5)

        # Set time position (where in the track to resume)
        # player.time_pos = state_data['time_pos']
        mp.time_pos = time_pos
        # mp.wait_until_playing()

    # mp.play()


def play():
    print('play')
    print(playlist)
    # noise.loadlist(noiseplaylist)
    # mpv.
    # mp.loadlist(playlist)
    restoresongandpos()
    noise.loadlist(noiseplaylist)
    # mp.play()


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

        # mpv.p

        # mp = MPlayer()
        # noise = MPlayer()

        # mp.loadlist('/Users/peppe/Music/Ripped/Hiphop/playlist.txt')
        # mp.stop()

        # mpv.command(play='backward')
        # mpv.play()

        noiseplaylist = makeplaylist('noise')
        print(noiseplaylist)
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
    save_playlist_state(mp.time_pos)
    print('då')
