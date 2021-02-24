import unittest
import sys
import time
import threading
sys.path.append("../build/open62541")
import ua_types
from intermediateApi import ffi, lib

# reads a node from the server and verifies the id and the status code
def test_read_node_id_attribute(self):
    print("Start of test_read_node_id_attribute")
    parent_node_id = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 85))
    res = self.client.read_node_id_attribute(parent_node_id)
    self.assertFalse(lib.UA_StatusCode_isBad(res.status_code))
    self.assertEqual(str(res.status_code), "0")
    self.assertEqual(str(res.out_node_id.identifier.numeric), "85")
    print("End of test_read_node_id_attribute")