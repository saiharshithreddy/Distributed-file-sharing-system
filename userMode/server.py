import sys
sys.path.append('../')

import fileIO.server as server
import heartbeat.heartbeat_server as hb_server

import threading

t = threading.Thread(target=hb_server.serve())
t.start()

server.serve()