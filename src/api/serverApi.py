# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import lib, ffi


class UaServer:
    def __init__(self, config=None):
        if config is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        else:
            self.ua_server = lib.UA_Server_newWithConfig(config)

    def run(self, running):
        return lib.UA_Server_run(self.ua_server, [running])

    def run_shutdown(self):
        return lib.UA_Server_run_shutdown(self.ua_server)

    def getConfig(self):
        return lib.UA_Server_getConfig(self.ua_server)

    def run_startup(self):
        return lib.UA_Server_run_startup(self.ua_server)

    def run_iterate(self, wait_internal):
        return lib.UA_Server_run_iterate(self.ua_server, wait_internal)

    #    def delete(self):
    #        return lib.UA_Server_delete(self.ua_server)

    def set_minimal_config(self, port_number, certificate):
        return lib.UA_ServerConfig_setMinimal(self.getConfig(), port_number, certificate)

    def set_default_config(self):
        return lib.UA_ServerConfig_setDefault(self.getConfig())