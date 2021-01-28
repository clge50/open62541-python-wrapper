import sys
sys.path.append("../build/api")
import serverApi as api

# Create new server object
server = api.lib.UA_Server_new()

# Set minimal usable config
api.lib.UA_ServerConfig_setDefault(api.lib.UA_Server_getConfig(server))

# Set server to always run
# Note: must be passed as pointer to bool
# thus we use an array
running = [True]

# Start server
retval = api.lib.UA_Server_run(server, running)

# TODO: Shutdown server gracefully