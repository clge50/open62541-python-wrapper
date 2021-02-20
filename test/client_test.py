import pytest
import sys
import time
import threading
sys.path.append("../build/open62541")
import serverApi
import clientApi
from intermediateApi import ffi, lib


class TestClientApi:
    server = None
    client = None
    running = [True]
    thread = None

    def setup_method(self):
        print("start of setUp")
        self.server = serverApi.UaServer()
        self.thread = threading.Thread(target=self.server.run, args=[self.running], daemon=True)
        self.thread.start()
        time.sleep(2)

        self.client = clientApi.UaClient()
        self.client.connect("opc.tcp://127.0.0.1:4840/")
        print("end of setUp")

    def teardown_method(self):
        print("start of tearDown")
        self.server.run_shutdown()
        self.thread.join(1)
        self.server = None
        self.client = None
        print("end of tearDown")

    # basic methods tests

    # def test_connect(self):

    # def test_disconnect(self):

    # def test_connect_secure_channel(self):

    # def test_disconnect_secure_channel(self):

    # def test_service_read(self):

    # def test_service_write(self):

    # def test_service_call(self):

    # def test_service_add_nodes(self):

    # def test_service_add_references(self):

    # def test_service_delete_nodes(self):

    # def test_service_delete_references(self):

    # def test_service_browse(self):

    # def test_service_browse_next(self):

    # def test_service_translate_browse_paths_to_node_ids(self):

    # def test_service_register_node(self):

    # def test_service_unregister_node(self):

    # read service tests

    # reads a node from the server and verifies the id and the status code
    def test_read_node_id_attribute(self):
        print("Start of test_read_node_id_attribute")
        parent_node_id = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 85))
        res = self.client.read_node_id_attribute(parent_node_id)
        assert not lib.UA_StatusCode_isBad(res.status_code)
        assert str(res.status_code) == "0"
        assert str(res.out_node_id.identifier.numeric) == "85"
        print("End of test_read_node_id_attribute")

    # def test_read_node_class_attribute(self):

    # def test_read_browse_name_attribute(self):

    # def test_read_display_name_attribute(self):

    # def test_read_description_attribute(self):

    # def test_read_write_mask_attribute(self):

    # def test_read_user_write_mask_attribute(self):

    # def test_read_is_abstract_attribute(self):

    # def test_read_symmetric_attribute(self):

    # def test_read_inverse_name_attribute(self):

    # def test_read_contains_no_loops_attribute(self):

    # def test_read_event_notifier_attribute(self):

    # def test_read_value_attribute(self):

    # def test_read_data_type_attribute(self):

    # def test_read_value_rank_attribute(self):

    # def test_read_array_dimensions_attribute(self):

    # def test_read_access_level_attribute(self):

    # def test_read_user_access_level_attribute(self):

    # def test_read_minimum_sampling_interval_attribute(self):

    # def test_read_executable_attribute(self):

    # def test_read_user_executable_attribute(self):

    # write service tests

    # def test_write_node_id_attribute(self):

    # def test_write_node_class_attribute(self):

    # def test_write_browse_name_attribute(self):

    # def test_write_display_name_attribute(self):

    # def test_write_description_attribute(self):

    # def test_write_write_mask_attribute(self):

    # def test_write_user_write_mask_attribute(self):

    # def test_write_is_abstract_attribute(self):

    # def test_write_symmetric_attribute(self):

    # def test_write_inverse_name_attribute(self):

    # def test_write_contains_no_loops_attribute(self):

    # def test_write_event_notifier_attribute(self):

    # def test_write_value_attribute(self):

    # def test_write_data_type_attribute(self):

    # def test_write_value_rank_attribute(self):

    # def test_write_array_dimensions_attribute(self):

    # def test_write_access_level_attribute(self):

    # def test_write_user_access_level_attribute(self):

    # def test_write_minimum_sampling_interval_attribute(self):

    # def test_write_executable_attribute(self):

    # def test_write_user_executable_attribute(self):

    # misc service test

    # def test_call(self):

    # def test_add_reference(self):

    # def test_delete_reference(self):

    # def test_delete_node(self):

    # def test_add_variable_node(self):

    # def test_add_variable_type_node(self):

    # def test_add_object_node(self):

    # def test_add_object_type_node(self):

    # def test_add_view_node(self):

    # def test_add_reference_type_node(self):

    # def test_add_data_type_node(self):

    # def test_add_method_node(self):

    # utils test

    # def test_get_config(self):

    # def test_set_default_config(self):

    # def test_find_data_type(self):

    # def test_get_endpoints(self):

    # def test_find_servers(self):
