from ua import *
import signal

pump_type_id = UaNodeId(1, 1001)
server = UaServer()


def manually_define_pump(server: UaServer):
    o_attr = UA_ATTRIBUTES_DEFAULT.OBJECT
    pump_id = server.add_object_node(UaNodeId.NULL(), UA_NS0ID.OBJECTSFOLDER, UA_NS0ID.ORGANIZES,
                                     UaQualifiedName(1, "Pump (Manual)"),
                                     UA_NS0ID.BASEOBJECTTYPE, o_attr).out_node

    mn_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    manufacturer_name = UaString("Pump King Ltd.")
    mn_attr.data_value.data = manufacturer_name
    mn_attr.display_name = UaLocalizedText("en-US", "ManufacturerName")
    result = server.add_variable_node(UaNodeId.NULL(), pump_id, UA_NS0ID.HASCOMPONENT,
                                      UaQualifiedName(1, "ManufacturerName"),
                                      UA_NS0ID.BASEDATAVARIABLETYPE, mn_attr)

    model_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    model_name = UaString("Mega Pump 3000")
    model_attr.data_value.data = model_name
    model_attr.display_name = UaLocalizedText("en-US", "ModelName")
    server.add_variable_node(UaNodeId.NULL(), pump_id, UA_NS0ID.HASCOMPONENT,
                             UaQualifiedName(1, "ModelName"),
                             UA_NS0ID.BASEDATAVARIABLETYPE, model_attr)

    status_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    status_attr.data_value.data = UaBoolean(True)
    status_attr.display_name = UaLocalizedText("en-US", "Status")
    server.add_variable_node(UaNodeId.NULL(), pump_id, UA_NS0ID.HASCOMPONENT,
                             UaQualifiedName(1, "Status"),
                             UA_NS0ID.BASEDATAVARIABLETYPE, status_attr)

    rpm_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    rpm_attr.data_value.data = UaDouble(50.0)
    rpm_attr.display_name = UaLocalizedText("en-US", "MotorRPM")
    server.add_variable_node(UaNodeId.NULL(), pump_id, UA_NS0ID.HASCOMPONENT,
                             UaQualifiedName(1, "MotorRPMs"),
                             UA_NS0ID.BASEDATAVARIABLETYPE, rpm_attr)


def define_object_types(server: UaServer):
    dt_attr = UA_ATTRIBUTES_DEFAULT.OBJECT_TYPE
    dt_attr.display_name = UaLocalizedText("en-US", "DeviceType")
    device_type_id = server.add_object_type_node(UaNodeId.NULL(), UA_NS0ID.BASEOBJECTTYPE,
                                                 UA_NS0ID.HASSUBTYPE,
                                                 UaQualifiedName(1, "DeviceType"),
                                                 dt_attr).out_node

    mn_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    mn_attr.display_name = UaLocalizedText("en-US", "ManufacturerName")
    manufacturer_name_id = server.add_variable_node(UaNodeId.NULL(), device_type_id, UA_NS0ID.HASCOMPONENT,
                                                    UaQualifiedName(1, "ManufacturerName"),
                                                    UA_NS0ID.BASEDATAVARIABLETYPE,
                                                    mn_attr).out_node

    server.add_reference(manufacturer_name_id, UA_NS0ID.HASMODELLINGRULE,
                         UaExpandedNodeId(0, UA_NS0ID.MODELLINGRULE_MANDATORY.identifier), UaBoolean(True))

    model_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    model_attr.display_name = UaLocalizedText("en-US", "ModelName")
    server.add_variable_node(UaNodeId.NULL(), device_type_id, UA_NS0ID.HASCOMPONENT,
                             UaQualifiedName(1, "ModelName"),
                             UA_NS0ID.BASEDATAVARIABLETYPE,
                             model_attr)

    pt_attr = UA_ATTRIBUTES_DEFAULT.OBJECT_TYPE
    pt_attr.display_name = UaLocalizedText("en-US", "PumpType")
    result = server.add_object_type_node(pump_type_id, device_type_id,
                                         UA_NS0ID.HASSUBTYPE,
                                         UaQualifiedName(1, "PumpType"),
                                         pt_attr)

    status_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    status_attr.display_name = UaLocalizedText("en-US", "Status")
    status_attr.value_rank = UaValueRanks.SCALAR
    status_id = server.add_variable_node(UaNodeId.NULL(), pump_type_id, UA_NS0ID.HASCOMPONENT,
                                         UaQualifiedName(1, "Status"),
                                         UA_NS0ID.BASEDATAVARIABLETYPE,
                                         status_attr).out_node

    server.add_reference(status_id, UA_NS0ID.HASMODELLINGRULE,
                         UaExpandedNodeId(0, UA_NS0ID.MODELLINGRULE_MANDATORY.identifier), UaBoolean(True))

    rpm_attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    rpm_attr.display_name = UaLocalizedText("en-US", "MotorRPM")
    server.add_variable_node(UaNodeId.NULL(), pump_type_id, UA_NS0ID.HASCOMPONENT,
                             UaQualifiedName(1, "MotorRPMs"),
                             UA_NS0ID.BASEDATAVARIABLETYPE,
                             rpm_attr)


def add_pump_object_instance(server: UaServer, name):
    o_attr = UA_ATTRIBUTES_DEFAULT.OBJECT
    o_attr.display_name = UaLocalizedText("en-US", name)
    result = server.add_object_node(UaNodeId.NULL(), UA_NS0ID.OBJECTSFOLDER,
                                    UA_NS0ID.ORGANIZES, UaQualifiedName(1, name), pump_type_id, o_attr)
    print(result.out_node)


def pump_type_constructor(server: UaServer, session_id: UaNodeId, session_context: Void, type_id: UaNodeId,
                          type_context: Void, node_id: UaNodeId, node_context: Void):
    UaLogger().info(UaLogCategory.USERLAND(), "New pump created")
    rpe = UaRelativePathElement()
    rpe.reference_type_id = UA_NS0ID.HASCOMPONENT
    rpe.is_inverse = UaBoolean(False)
    rpe.include_subtypes = UaBoolean(False)
    rpe.target_name = UaQualifiedName(1, "Status")

    bp = UaBrowsePath()
    bp.starting_node = node_id
    bp.relative_path.elements_size = SizeT(1)
    bp.relative_path.elements = rpe

    bpr = server.translate_browse_path_to_node_ids(bp)
    if bpr.status_code != UA_STATUSCODES.GOOD or bpr.targets_size < 1:
        return UaStatusCode(bpr.status_code)

    value = UaVariant()
    value.data = UaBoolean(True)
    server.write_value(bpr.targets.target_id.node_id, value)

    return UA_STATUSCODES.GOOD


def add_pump_type_constructor(server: UaServer):
    lifecycle = UaNodeTypeLifecycle()
    lifecycle.constructor = pump_type_constructor
    server.set_node_type_lifecycle(pump_type_id, lifecycle)


def stop_handler(arg1, arg2):
    UaLogger().info(UaLogCategory.SERVER(), "received ctrl-c")
    server.running = False


def main():
    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)
    manually_define_pump(server)
    define_object_types(server)
    add_pump_object_instance(server, "pump2")
    add_pump_object_instance(server, "pump3")
    add_pump_type_constructor(server)
    add_pump_object_instance(server, "pump4")
    add_pump_object_instance(server, "pump5")
    server.run()


if __name__ == '__main__':
    main()
