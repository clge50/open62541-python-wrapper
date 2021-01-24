import sys
sys.path.append("../")
import api

client = api.UaClient()
api.UaClient.setDefaultConfig(client.getConfig())
retval = client.connect(b"opc.tcp://christian-ThinkPad:4840/")

if retval != api.StatusCode.good():
	print("An error occurred. stopping client")
	quit()

value = api.Variant()

nodeId = api.Utils.nodeIdNumeric(0, api.Utils.serverStatusCurrentTimeId())
retval = client.readValueAttribute(nodeId, value);

if retval == api.StatusCode.good() and False == value.hasScalarType(api.DataType.dateTime()):
	rawDate = api.Utils.castToDateTime(value)
	dts = api.DateTime(rawDate)
	api.Log.loginfo(api.Log.logStdout(), 
		api.Log.logCategoryUserland(), 
		"date is: {}\n".format(str(dts)))
