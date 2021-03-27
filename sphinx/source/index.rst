Introduction
====================================================

What is wrappy(06)?
----------------------
Wrappy(o6) is a python binding for open62541 (http://open62541.org).
While wrappy(06) tries to be truthful to it's roots in terms of handling it still aims at offering some quality of life improvements and getting rid of certain c typical conventions which feel weird in python.
If you are already familiar with open62541 and know some basic python you'll hopefully feel right at home in wrappy(06) we hope you'll feel right at home in Wrappy(06) and can make use of the vast range of available python libraries while still being able to use the well established open62541 as a backend.

License
--------
wrappy(o6) (same as open62541 itself) is licensed under the Mozilla Public License v2.0 (MPLv2)(https://www.mozilla.org/en-US/MPL/2.0/).

open62541 python wrapper Features
---------------------------------

.. Warning::
    Please be aware that wrappy(06) is still in an early development phase. Please refer to :ref:`Open issues<Open issues>` for more information regarding open62541 features which are not available yet as well as general limitations and issues.

Getting started
=================

Dependencies
---------------------------------
* python 3.6 or newer (tested with 3.6, 3.7, 3.8)
* pip
* cffi (installable via pip)

Installation
---------------------------------
After you made sure that all dependencies are installed, to install wrappy(06) run the python script `make.py`.
It will create a package `build/wrappy_o6` which holds all necessary modules to use wrappy(06).
Simply import the module `ua` from `build/wrappy_o6` and you are good to go!


First steps / learning how to use wrappy(06)
-------------------------------------------------
Please refer to the `examples` directory to see some examples of the usage of wrappy(06). The tutorials named `example_tutorial_` aim to stick closely to the tutorials of open62541.

Information for wrappy(o6) developers
====================================================

.. automodule:: ua_types_parent
   :members:
   :special-members: __init__

Open issues
------------

Currently there still a lot of open issues which need to be addressed in order to ensure a satisfying usability and stability of wrappy(o6):

* tests are still very lacking. There are currently only tests for the UaClient and they are not semantically sound. So there is definitely a need for tests for the UaClient, UaServer and UaTypes.
* The current handling of callbacks / function pointers has some major issues / restrictions. A reimplementation or adaptions to improve usability should be considered. Please refer to the :ref:`Callbacks<Callbacks>` for additional information.
* User generated types are not yet supported. Please find a draft / outline of a possible implementation strategy in the chapter :ref:`User generated types<User generated types>`.
* Historizing is not supported yet
* Pub/sub is not supported yet
* build script has not been tested under systems other than Ubuntu 18.04/20.04
* the documentation needs to be improved to smoothen the experience for new users. Some topics worth mentioning:
    * UaList handling
    * Void type handling
    * casting
* UaClientConfig is still missing some fields for lower level configurations


Callbacks
-----------
.. automodule:: ua_client
   :members:
    _ClientCallback

.. automodule:: ua_server
   :members:
    _ServerCallback

.. automodule:: ua_types_serverconfig
   :members:
    UaServerConfig

User generated types
---------------------

TODO