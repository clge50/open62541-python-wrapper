import time

from ua import UaBoolean, UaServer

# Create new server object, default set
server = UaServer()
server.run_async()

time.sleep(15)

server.running = False
