from functools import reduce

from cffi import FFI
import os
from shutil import copytree

dirname = os.path.dirname(os.path.abspath(__file__))

def setup_open62541():
    open62541_repo = r"https://github.com/open62541/open62541.git"

    os.chdir(dirname)
    os.system("git clone " + open62541_repo)
    os.mkdir(dirname + r"/open62541/build")
    os.chdir(dirname + r"/open62541/build")
    os.system("cmake .. -DUA_ENABLE_AMALGAMATION=TRUE")
    os.system("make")
    os.chdir(dirname)


def generate_api():
    decl_files_list = ["types", "types_generated", "util", "log", "client", "client_highlevel", "client_config_default", "server"]
    decls_list = []

    for file_name in decl_files_list:
        with open(dirname + r"/src/definitions/" + file_name) as file_handler:
            decls_list.append(file_handler.read())

    cffi_input = reduce(lambda s1, s2: s1 + "\n" + s2, decls_list)

    ffibuilder = FFI()
    ffibuilder.set_source("intermediateApi",
                          r"""#include "open62541.h"
		""",
                          include_dirs=[dirname + r"/open62541/build"],
                          library_dirs=[dirname + r"/open62541/build/bin"],
                          libraries=['open62541'])

    ffibuilder.cdef(cffi_input)
    os.mkdir("build")
    copytree(dirname + r"/src/api", dirname + r"/build/open62541")
    os.chdir(dirname + r"/build/open62541/")
    ffibuilder.compile(verbose=True)
    print("finished building intermediateApi")


# setupOpen62541()
os.chdir(dirname)
generate_api()
