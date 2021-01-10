import sys
sys.path.append("../src/")
import api

client = api.UaClient()
api.UaClient.setDefaultConfig(client.getConfig())
retval = client.connect(b"opc.tcp://127.0.0.1:16664")

if retval != api.StatusCode.good():
	print("An error occurred. stopping client")
	quit()

value = api.Variant()

nodeId = api.Utils.nodeIdNumeric(0, api.Utils.serverStatusCurrentTimeId())
retval = client.readValueAttribute(nodeId, value);

if retval == api.StatusCode.good() and False == value.hasScalarType(api.DataType.dateTime()):
	rawDate = api.Utils.castToDateTime(value)
	dts = api.Utils.uaDateTimeToStruct(rawDate)
	api.Log.loginfo(api.Log.logStdout(), 
		api.Log.logCategoryUserland(), 
		b"date is: %u-%u-%u %u:%u:%u.%03u\n",
		api.Utils.uint16(dts.day), 
		api.Utils.uint16(dts.month),
		api.Utils.uint16(dts.year), 
		api.Utils.uint16(dts.hour), 
		api.Utils.uint16(dts.min), 
		api.Utils.uint16(dts.sec), 
		api.Utils.uint16(dts.milliSec)