import unittest
import sys
import time

sys.path.append("../build/open62541")
import serverApi
from intermediateApi import ffi, lib


class TestServerApi(unittest.TestCase):
    server = None

    def setUp(self):
        pass

    def tearDown(self):
        # TODO: stop server
        server = None
        pass

    # tests
