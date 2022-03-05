import rpyc

class ClientService(rpyc.Service):
    def exposed_foo(self):
        return "foo"

conn = rpyc.connect("localhost", 12345, service = ClientService)

# a = conn.root.bar('hej')

conn.root.loadfile('/Users/peppe/Music/Ripped/Hiphop /playlist.txt')

# print(a)

