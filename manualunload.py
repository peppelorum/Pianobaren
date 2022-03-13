import rpyc

conn = rpyc.connect("localhost", 12345)
unload = rpyc.async_(conn.root.unload)
unload()

