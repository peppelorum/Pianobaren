import random
import rpyc

lists = ['0014030686', '0009148262']

conn = rpyc.connect("localhost", 12345)
loadtag = rpyc.async_(conn.root.loadtag)
a = loadtag(random.choice(lists))
