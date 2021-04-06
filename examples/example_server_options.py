# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from time import sleep
from signal import signal, SIGINT, SIGTERM

from ua import *


def get_default_server():
    """Per Default this returns a server with exactly one endpoint on localhost, port 4840."""
    return UaServer()


def get_server_with_port():
    """This returns a server with exactly one endpoint with specified port on localhost."""
    return UaServer(4841)


def get_server_with_hostname_and_port():
    """This returns a server with exactly one endpoint with specified port and hostname."""
    return UaServer(("localhost", 4841))


def get_server_from_config():
    """This returns a server with a specified config.
    Unfortunately the open62541 builder functions for server configs are not supported yet."""
    config = UaServerConfig.get_default()
    return UaServer(config)


def use_server_run(server: UaServer):
    """The method ``run()`` is blocking so it has to be called at the end of a script.
    With a signal handler the server can be stopped (in this example via sigint)"""
    server.run()


def use_server_run_async(server: UaServer):
    """The method ``run_async()`` invokes ``run()`` in another thread (returned by the method) so it is non-blocking.
    Per default the thread is not a daemon (this can be changed by passing True as second argument)"""
    t = server.run_async()
    print("press enter if you want to stop")
    input()
    server.running = False
    t.join()

def use_server_run_iterate(server: UaServer):
    """To the method ``run()`` implicitly calls ``run_startup()`` and then in a loop ``run_iterate()``
    as long as ``running`` is True. This can also be done explicitly as follows."""
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
