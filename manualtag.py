import rpyc

conn = rpyc.connect("localhost", 12345)
loadtag = rpyc.async_(conn.root.loadtag)
a = loadtag('0009148262')

