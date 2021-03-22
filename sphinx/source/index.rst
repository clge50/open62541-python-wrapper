Introduction
====================================================

wrappy(o6) is a python binding for open62541 (http://open62541.org)

wrappy(o6) (same as open62541 itself) is licensed under the Mozilla Public License v2.0 (MPLv2).

open62541 python wrapper Features
---------------------------------
wrappy(o6) is still very much work in process. It allows to handle most of the basic ua data types which are
introduced by open62541 and allows to build basic clients and servers and access their respective services. Low level configurations
however are not fully available yet and there are still certain limitations in regards to callback functions.
Furthermore the build process currently has not been adapted for non linux machines and has only been tested with ubuntu 20.04.

dependencies
---------------------------------
* python 3.6 or newer (tested with 3.6, 3.7, 3.8)
* pip
* cffi (`pip install cffi`)

installation
---------------------------------
To install wrappy(06) run the python script `make.py`. It will create a package `build/open62541` which holds all necessary modules to use wrappy(06).
Simply import the module `ua` and you are good to go!

UaType
====================================================

.. automodule:: ua_types_parent
   :members:
   :special-members: __init__

Callbacks
====================================================
.. automodule:: ua_client
   :members:
    _ClientCallback

.. automodule:: ua_server
   :members:
    _ServerCallback

.. automodule:: ua_types_serverconfig
   :members:
    UaServerConfig
