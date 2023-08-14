import rpyc

conn = rpyc.connect("localhost", 12345)
loadtag = rpyc.async_(conn.root.pitch)
loadtag()
