from cffi import FFI
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))


def setupOpen62541():
	open62541Repo = r"https://github.com/open62541/open62541.git"

	os.chdir(dirname)
	os.system("git clone " + open62541Repo)
	os.system("mkdir ./open62541/build")
	os.chdir(dirname + r"/open62541/build")
	os.system("cmake .. -DUA_ENABLE_AMALGAMATION=TRUE")
	os.system("make")
	os.chdir(dirname)

def generateApi():
	with open("./src/definitions/types") as file_handler:
		types = file_handler.read()

	with open("./src/definitions/types_generated") as file_handler:
		types_generated = file_handler.read()

	with open("./src/definitions/util") as file_handler:
		util = file_handler.read()

	with open("./src/definitions/client") as file_handler:
		client = file_handler.read()

	with open("./src/definitions/client_highlevel") as file_handler:
		client_highlevel = file_handler.read()
		
	with open("./src/definitions/client_config_default") as file_handler:
		client_config_default = file_handler.read()


	cffi_input = types + "\n" + types_generated + "\n" + util + "\n" + client + "\n" + client_highlevel + "\n" + client_config_default


	ffibuilder = FFI()
	ffibuilder.set_source("intermediateApi",
		r"""#include "open62541.h"
		""",
		include_dirs=[dirname + r"/open62541/build"],
		library_dirs=[dirname + r"/open62541/build/bin"],
		libraries=['open62541'])

	ffibuilder.cdef(cffi_input)
	os.system("mkdir build")
	os.chdir(dirname + r"/build")
	os.system("cp -R ./../src/api ./")
	os.chdir(dirname + r"/build/api/")
	ffibuilder.compile(verbose=True)
	print("finished building intermediateApi")
	
	

#setupOpen62541()
os.chdir(dirname)
generateApi()
