import rpyc
from mplayer import MPlayer
from rpyc.utils.server import ThreadedServer # or ForkingServer
import subprocess





class ServerService(rpyc.Service):
    def on_connect(self, conn):
        self._conn = conn

    def exposed_loadfile(self, arg):
        print(arg)
        # a = subprocess.run(["cd "+ arg +"&& find -type f -iname *.mp3 > playlist.txt"])

        # print(a)

        mp.loadlist(arg)

        # return self._conn.root.foo() + arg

# conn = rpyc.connect("localhost", 12345, service = ServerService)



if __name__ == "__main__":
    server = ThreadedServer(ServerService, port = 12345)


    MPlayer.populate()
    try:
        mp = MPlayer()
        import readline
        readline.parse_and_bind('tab: complete')
        import rlcompleter
        mp.loadlist('/Users/peppe/Music/Ripped/House etc/playlist.txt')


        mp.command("volume 50 1")

    finally:
        print('knas')
        # mp.command('quit')

    server.start()
    print('då')