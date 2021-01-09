# not working properly
import sys
import os
import re

dirname = os.path.dirname(os.path.abspath(__file__))
file = open(dirname + r"/open62541/build/open62541.h", "r")
extractedDefs = re.findall('(\n.*UA_EXPORT.*?;)|(\n.*typedef.*?;)', file.read())

print(" ".join(map(lambda a: a[0] + a[1], extractedDefs)))
#print(type(extractedDefs[0]))

#for inst in extractedDefs:
#	print(inst)
