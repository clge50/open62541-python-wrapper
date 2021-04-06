# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import time

from ua import UaBoolean, UaServer

# Create new server object, default set
server = UaServer()
server.run_async()

time.sleep(15)

server.running = False
