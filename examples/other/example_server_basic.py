import sys
import time
from ua import UaBoolean, UaServer

sys.path.append("../../build/open62541")


# Create new server object
server = UaServer()

# Start server
ret_val = server.run(UaBoolean(True))

time.sleep(100)
server.run_shutdown()
print("server shut down after 100s")
