import sys
import time
sys.path.append("../build/open62541")
import serverApi as api

# Create new server object
server = api.UaServer()

# Start server
retval = server.run_async([True])

time.sleep(100)
server.run_shutdown()
print("server shut down after 60s")