from time import sleep
import sys
from signal import signal, SIGINT, SIGTERM

sys.path.append("../build/wrappy_o6")
from ua import *


# per default one endpoint on localhost, port 4840
def get_default_server():
    return UaServer()


# server with one endpoint with specified port on localhost
def get_server_with_port():
    return UaServer(4841)


# server with one endpoint with specified port and hostname
def get_server_with_hostname_and_port():
    return UaServer(("localhost", 4841))


# server from server config
def get_server_from_config():
    config = UaServerConfig.get_default()
    return UaServer(config)


def use_server_run(server: UaServer):
    # run() is blocking so it has to be called at the end of a script.
    # With the the signal handler the server can be stopped via sigint
    server.run()


def use_server_run_async(server: UaServer):
    # run_async() invokes run() in a another thread (returned by the method) so it it is non-blocking.
    # per default the thread is not a daemon (this can be changed by passing True)
    t = server.run_async()
    print("press enter if you want to stop")
    input()
    server.running = False
    t.join()

def use_server_run_iterate(server: UaServer):
    server.run_startup()
    server.running = True
    while server.running:
        server.run_iterate()
        sleep(0.5)


def stop_handler(arg1, arg2):
    UaLogger().info(UaLogCategory.SERVER(), "received ctrl-c")
    s.running = False


if __name__ == '__main__':
    signal(SIGINT, stop_handler)
    signal(SIGTERM, stop_handler)

    s = get_server_with_hostname_and_port()

    # use_server_run(s)
    # use_server_run_async(s)
    use_server_run_iterate(s)
