import sys
import time
import signal

sys.path.append("../build/open62541")
from ua import UaBoolean, UaServer


def handler(sig, frame):
    print("sigint")
    server.running = False


signal.signal(signal.SIGINT, handler)
# Create new server object, default set
server = UaServer()

# Start server
# ret_val = server.run(UaBoolean(True))
# print(f"server run called with {ret_val}")

while True:
    i = 0
