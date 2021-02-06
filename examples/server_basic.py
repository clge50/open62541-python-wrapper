import sys
import time

sys.path.append("../build/open62541")
import serverApi

# Create new server object
server = serverApi.UaServer()

# Start server
retval = server.run([True])

time.sleep(100)
server.run_shutdown()
print("server shut down after 60s")
