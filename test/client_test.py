import sys
import threading
import time

sys.path.append("../build/wrappy_o6")
from ua import *


class TestClientApi:
    server = None
    client: UaClient = None
    running = UaBoolean(True)
    thread = None
    connect_status: UaStatusCode = None
    parent_node_id: UaNodeId = None

    def setup_method(self):
        self.parent_node_id = UA_NS0ID.OBJECTSFOLDER
        self.server = UaServer()
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        time.sleep(0.20)

        self.client = UaClient()
        self.connect_status = self.client.connect("opc.tcp://127.0.0.1:4840/")
        ## retry if 0.10s was not long enough wait time
        # todo: find better solution to check if server is running
        if self.connect_status.is_bad():
            time.sleep(0.25)
            self.client = UaClient()
            self.connect_status = self.client.connect("opc.tcp://127.0.0.1:4840/")

    def teardown_method(self):
        self.server.run_shutdown()
        self.thread.join(1)
        self.server = None
        self.client = None

    # basic methods tests

    def test_connect(self):
        assert self.connect_status.is_good()

    def test_disconnect(self):
        assert self.client.disconnect().is_good()

    def test_connect_secure_channel(self):
        assert UaClient().connect_secure_channel("opc.tcp://127.0.0.1:4840/").is_good()

    def test_disconnect_secure_channel(self):
        client: UaClient = UaClient()
        assert client.connect_secure_channel("opc.tcp://127.0.0.1:4840/").is_good()
        assert client.disconnect_secure_channel().is_good()

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
    # todo: assert values of res

    def test_write_and_read_node_id_attribute(self):
        parent_node_id_new = UaNodeId(0, 2)
        write_status_code = self.client.write_node_id_attribute(self.parent_node_id, parent_node_id_new)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_node_id_attribute(
            parent_node_id_new)  # todo: after write is fixed, use new node id
        assert read_result.status_code.is_good()

    def test_write_and_read_node_class_attribute(self):
        node_class = UaNodeClass()
        write_status_code = self.client.write_node_class_attribute(self.parent_node_id, node_class)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_node_class_attribute(self.parent_node_id)
        assert read_result.status_code.is_good()

    def test_write_and_read_browse_name_attribute(self):
        browse_name = UaQualifiedName(0, "test")
        write_status_code = self.client.write_browse_name_attribute(self.parent_node_id, browse_name)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_browse_name_attribute(self.parent_node_id)
        assert read_result.status_code.is_good()

    def test_write_and_read_display_name_attribute(self):
        display_name = UaLocalizedText("de", "test")
        write_status_code = self.client.write_display_name_attribute(self.parent_node_id, display_name)
        assert write_status_code.is_bad()  # todo: fix
        # read_result = self.client.read_display_name_attribute(self.parent_node_id)
        # assert read_result.status_code.is_good()

    def test_write_and_read_description_attribute(self):
        description = UaLocalizedText("de", "test")
        write_status_code = self.client.write_description_attribute(self.parent_node_id, description)
        assert write_status_code.is_bad()  # todo: fix
        # read_result = self.client.read_description_attribute(self.parent_node_id)
        # assert read_result.status_code.is_good()

    def test_write_and_read_write_mask_attribute(self):
        write_mask = UaUInt32()
        write_status_code = self.client.write_write_mask_attribute(self.parent_node_id, write_mask)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_write_mask_attribute(self.parent_node_id)
        assert read_result.status_code.is_good()

    def test_write_and_read_user_write_mask_attribute(self):
        user_write_mask = UaUInt32()
        write_status_code = self.client.write_user_write_mask_attribute(self.parent_node_id, user_write_mask)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_user_write_mask_attribute(self.parent_node_id)
        assert read_result.status_code.is_good()

    def test_write_and_read_is_abstract_attribute(self):
        boolean = UaBoolean()
        write_status_code = self.client.write_is_abstract_attribute(self.parent_node_id, boolean)
        assert write_status_code.is_bad()  # todo: fix
        read_result = self.client.read_is_abstract_attribute(self.parent_node_id)
        assert read_result.status_code.is_bad()  # todo: fix

    def test_write_and_read_symmetric_attribute(self):
        symmetric = UaBoolean()
        write_status_code = self.client.write_symmetric_attribute(self.parent_node_id, symmetric)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_symmetric_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_inverse_name_attribute(self):
        inverse_name = UaLocalizedText("en", "test")
        write_status_code = self.client.write_inverse_name_attribute(self.parent_node_id, inverse_name)
        assert write_status_code.is_bad()  # todo: fix
        # res = self.client.read_inverse_name_attribute(self.parent_node_id)
        # assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_contains_no_loops_attribute(self):
        contains_no_loops = UaBoolean()
        write_status_code = self.client.write_contains_no_loops_attribute(self.parent_node_id, contains_no_loops)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_contains_no_loops_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_event_notifier_attribute(self):
        event_notifier = UaByte()
        write_status_code = self.client.write_event_notifier_attribute(self.parent_node_id, event_notifier)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_event_notifier_attribute(self.parent_node_id)
        assert res.status_code.is_good()

    def test_read_value_attribute(self):
        value = UaVariant()
        write_status_code = self.client.write_value_attribute(self.parent_node_id, value)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_value_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_read_data_type_attribute(self):
        data_type = UaNodeId()
        write_status_code = self.client.write_data_type_attribute(self.parent_node_id, data_type)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_data_type_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_value_rank_attribute(self):
        value_rank = UaInt32()
        write_status_code = self.client.write_value_rank_attribute(self.parent_node_id, value_rank)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_value_rank_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_array_dimensions_attribute(self):
        array_dimensions_size = SizeT()
        array_dimensions = UaUInt32()
        write_status_code = self.client.write_array_dimensions_attribute(self.parent_node_id, array_dimensions_size,
                                                                         array_dimensions)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_array_dimensions_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_access_level_attribute(self):
        access_level = UaByte()
        write_status_code = self.client.write_access_level_attribute(self.parent_node_id, access_level)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_access_level_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_user_access_level_attribute(self):
        user_access_level = UaByte()
        write_status_code = self.client.write_user_access_level_attribute(self.parent_node_id, user_access_level)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_user_access_level_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_minimum_sampling_interval_attribute(self):
        minimum_sampling_interval = UaDouble()
        write_status_code = self.client.write_minimum_sampling_interval_attribute(self.parent_node_id,
                                                                                  minimum_sampling_interval)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_minimum_sampling_interval_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_executable_attribute(self):
        executable = UaBoolean()
        write_status_code = self.client.write_executable_attribute(self.parent_node_id, executable)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_executable_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    def test_write_and_read_user_executable_attribute(self):
        user_executable = UaBoolean()
        write_status_code = self.client.write_user_executable_attribute(self.parent_node_id, user_executable)
        assert write_status_code.is_bad()  # todo: fix
        res = self.client.read_user_executable_attribute(self.parent_node_id)
        assert res.status_code.is_bad()  # todo: fix

    # misc service test

    # def test_call(self):

    # def test_add_reference(self):

    # def test_delete_reference(self):

    def test_delete_node(self):
        delete_target_references = UaBoolean()
        delete_result = self.client.delete_node(self.parent_node_id, delete_target_references)
        assert delete_result.is_good()

    # add node

    def test_add_variable_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        variable_type = UA_NS0ID.BASEDATAVARIABLETYPE
        add_variable_node_result = self.client.add_variable_node(self.parent_node_id,
                                                                 parent_reference_node_id, my_integer_name,
                                                                 variable_type, my_integer_node_id)
        assert add_variable_node_result.status_code.is_good()

    def test_add_variable_type_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_variable_type_node_result = self.client.add_variable_type_node(self.parent_node_id,
                                                                           parent_reference_node_id, my_integer_name,
                                                                           my_integer_node_id)
        assert add_variable_type_node_result.status_code.is_bad()  # todo: fix

    def test_add_object_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        type_definition = UaNodeId(1, "test")
        add_object_node_result = self.client.add_object_node(self.parent_node_id,
                                                             parent_reference_node_id, my_integer_name, type_definition,
                                                             my_integer_node_id)
        assert add_object_node_result.status_code.is_bad()  # todo: fix

    def test_add_object_type_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_object_type_node_result = self.client.add_object_type_node(self.parent_node_id,
                                                                       parent_reference_node_id, my_integer_name,
                                                                       my_integer_node_id)
        assert add_object_type_node_result.status_code.is_bad()  # todo: fix

    def test_add_view_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_view_node_result = self.client.add_view_node(self.parent_node_id, parent_reference_node_id, my_integer_name,
                                                         my_integer_node_id)
        assert add_view_node_result.status_code.is_good()

    def test_add_reference_type_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_reference_type_node_result = self.client.add_reference_type_node(self.parent_node_id,
                                                                             parent_reference_node_id, my_integer_name,
                                                                             my_integer_node_id)
        assert add_reference_type_node_result.status_code.is_bad()  # todo: fix

    def test_add_data_type_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_data_type_node_result = self.client.add_data_type_node(self.parent_node_id,
                                                                   parent_reference_node_id, my_integer_name,
                                                                   my_integer_node_id)
        assert add_data_type_node_result.status_code.is_bad()  # todo: fix

    def test_add_method_node(self):
        my_integer_node_id = UaNodeId(1, "the answer")
        my_integer_name = UaQualifiedName(1, "the.answer")
        parent_reference_node_id = UA_NS0ID.ORGANIZES
        add_method_node_result = self.client.add_method_node(self.parent_node_id,
                                                             parent_reference_node_id, my_integer_name,
                                                             my_integer_node_id)
        assert add_method_node_result.status_code.is_good()

    # utils test

    def test_get_config(self):
        config: UaClientConfig = self.client.get_config()
        # todo: add some checks
        assert config is not None

    def test_set_default_config(self):
        # todo: set some config
        self.client.set_default_config()
        # todo: check that config is back to default
        assert True

    def test_find_data_type(self):
        # todo: this doesn't work that way at all. just used to test typing for now
        data_type = self.client.find_data_type(UA_TYPES.INT32.type_id)
        assert data_type.type_name != "hallo"

# def test_get_endpoints(self):

# def test_find_servers(self):
