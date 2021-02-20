import sys
import time
import pytest

sys.path.append("../build/open62541")
import serverApi
from intermediateApi import ffi, lib


class TestServerApi:
    server = None

    def setUp(self):
        pass

    def tearDown(self):
        # TODO: stop server
        server = None
        pass

    # tests
    def test_test(self):
    	assert True
