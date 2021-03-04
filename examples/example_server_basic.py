import sys
import time

sys.path.append("../build/open62541")
import serverApi
from ua import UaBoolean

# Create new server object
server = serverApi.UaServer()

# Start server
retval = server.run(UaBoolean(True))

time.sleep(100)
server.run_shutdown()
print("server shut down after 100s")
