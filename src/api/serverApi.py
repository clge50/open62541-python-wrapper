from intermediateApi import lib,ffi

class UaServer:
    def __init__(self):
        self.ua_server = lib.UA_Server_new()

    def UA_Server_run(server, running):
        return lib.UA_Server_run(self.ua_server, running)
    
    def UA_Server_run_shutdown(server):
        return lib.UA_Server_run_shutdown(self.server)

    def UA_Server_getConfig(server):
        return lib.UA_Server_getConfig(self.server)

    def UA_Server_run_startup(server):
        return lib.UA_Server_run_startup(self.server)

    def UA_Server_run_iterate(server, waitInternal):
        return lib.UA_Server_run_iterate(self.server, waitInternal)

    def UA_Server_delete(server):
        return lib.UA_Server_delete(self.server)
        
    def UA_Server_newWithConfig(config):
        return lib.UA_Server_newWithConfig(config)
    
    def UA_ServerConfig_setMinimal(config, portNumber, certificate):
        return lib.UA_ServerConfig_setMinimal(config, portNumber, certificate)

    def UA_ServerConfig_setDefault(config):
        return lib.UA_ServerConfig_setMinimal(config, 4840, NULL)