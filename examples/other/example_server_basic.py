# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

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
