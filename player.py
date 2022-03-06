import rpyc

conn = rpyc.connect("localhost", 12345)
# conn.root.loadfile('/Users/peppe/Music/Ripped/Cyberpunk/')
conn.root.loadtag('0014030686')
