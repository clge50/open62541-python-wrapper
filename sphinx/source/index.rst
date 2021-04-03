Introduction
====================================================

What is wrappy(o6)?
----------------------
Wrappy(o6) is a python binding for `open62541 <http://open62541.org`_.
While wrappy(o6) tries to be truthful to it's roots in terms of handling it still aims at offering some quality of life improvements and getting rid of certain c typical conventions which feel weird in python.
If you are already familiar with open62541 and know some basic python you'll hopefully feel right at home in wrappy(o6) we hope you'll feel right at home in Wrappy(o6) and can make use of the vast range of available python libraries while still being able to use the well established open62541 as a backend.

License
--------
wrappy(o6) (same as open62541 itself) is licensed under the `Mozilla Public License v2.0 (MPLv2) <https://www.mozilla.org/en-US/MPL/2.0/>`_.
The examples and tutorials are licensed under a `Creative Commons CCZero 1.0 Universal License <http://creativecommons.org/publicdomain/zero/1.0/>`_.

open62541 python wrapper Features
---------------------------------

.. Warning::
    Please be aware that wrappy(o6) is still in an early development phase. Please refer to :ref:`Open issues<Open issues>` for more information regarding open62541 features which are not available yet as well as general limitations and issues.

Getting started
=================

Dependencies
---------------------------------
* python 3.6 or newer (tested with 3.6, 3.7, 3.8)
* pip
* cffi (installable via pip)

Installation
---------------------------------
After you made sure that all dependencies are installed, to install wrappy(o6) run the python script `make.py`.
It will create a package `build/wrappy_o6` which holds all necessary modules to use wrappy(o6).
Simply import the module `ua` from `build/wrappy_o6` and you are good to go!


First steps / learning how to use wrappy(o6)
-------------------------------------------------
Please refer to the `examples` directory to see some examples of the usage of wrappy(o6). The tutorials named `example_tutorial_` aim to stick closely to the tutorials of open62541.

Information for wrappy(o6) developers
====================================================

General structure / architecture
------------------------------------

* 1:1 mapping of open62541 types to wrapped types
* A wrapped type has public components (python world) and hidden components (c world)
* improvements to handling via default values, "type guessing"

UaType
------------

.. automodule:: ua_types_parent
   :members:
   :special-members: __init__

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

Custom Data Types
---------------------

Wrappy(o6) lacks sufficient support of custom data types. To a limited extend it is already possible to create custom data types since all necessary c types (namely
``UA_DataType``, ``UA_DataTypeArray``, ``UA_ClientConfig.customDataTypes``, ``UA_DataTypeMember``, ``UA_DataType``) are available in wrappy(o6). Nevertheless an intuitive an efficient
handling has yet to be accomplished.

To achieve a satisfactory usability there are several issues to face, mostly regarding the typing in Python. In the following, the problems should be outlined and
possible approaches to their solution should be discussed.

In open62541 custom data types are representations of (structured) types such as structs, enums and unions. Mapping those types onto ``UA_DataTypeMembers`` and ``UA_DataTypes``
is quite straight forward. In python there is much more work to do.
Since python is highly dynamically typed it is harder to determine the structure of an object (and hence the offsets and paddings of its fields) by its class definition.
Even with the typing library, most of the type hints do not apply at runtime (they mostly are really just *hints*). As a consequence there is no equivalent to the c function
``offsetof()``. If the user should not be left with calculating the paddings all by themselves, a similar method – meaning a method which takes a class and returns the offsets
or rather paddings of the fields (instance variables) – must be implemented in Python.
We want to make a rough suggestion how this could be done (at least for custom data types based on namespace zero) and how to proceed to obtain the ``UaDataType``.

For sake of the following explanations let uns suppose we want to build a custom data type corresponding to a struct like this.

.. code-block:: c

    typedef struct {
        UA_Xxx field1;
        UA_Yyy field2;
        ...
    } SomeType;

How could this be translated to Python? One strategy could be using *NamedTuples*.


Calculate the paddings
^^^^^^^^^^^^^^^^^^^^^^^

The class `typing.NamedTuple <https://docs.python.org/3/library/typing.html>`_ provides struct-like easy to write objects with type hints.

.. code-block:: python

    class SomeType(NamedTuple):
        field1: UaXxx
        field2: UaYyy
        ...

It has to be examined whether and to which extend the type hints can be accessed via inflection at runtime.

What we want for the calculation of the offset and the further procedure, are the entries in ``UA_TYPES`` related to the UaType classes of the NamedTuple's fields.
Since every UaType class related to an entry in ``UA_TYPES`` knows that entry it would suffice to just get the UaType classes which are type hinted.
In terms of our example this is ``UaXxx._UA_TYPE`` (which would be a c macro like ``UA_TYPES_XXX``), ``UaYyy._UA_TYPE`` and so on.

If it is not possible to get these information via inflecting the type hints, there is another way to get the necessary information: The user has to provide default values for all fields.

.. code-block:: python

    class SomeType(NamedTuple):
        field1: UaXxx = UaXxx()
        field2: UaYyy = UaYyy()
        ...

Then ``SomeType`` can be passed to our method ``get_offset(...)``. The method ``get_offset(...)`` could invoke ``SomeType()`` which returns a NamedTuple – we call this instance ``some_type`` –
with all the default values. The fields of ``some_type`` could now be inflected with ``type(some_type.fieldX)``. We get the UaType classes and by this the ``UA_TYPES``.
Now we just need a mapping from the entries of ``UA_TYPES`` to the corresponding sizes. With this we could compute the paddings for all fields of our NamedTuple ``SomeType``
and return them as a dict of pairs ``fieldX: <padding in bytes>``.


With this information a user would be able to construct the ``UaDataTypeMembers`` and ``UaDataTypes`` similar to open62541. But still this would not feel like Python.
We rather want a static method – let us call it ``from_data_type_model(...)`` – in ``UaDataType`` which takes a class (f.e. a NamedTuple) and returns an instance of ``UaDataType``.

Construct the UaDataTypeMembers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our method ``from_data_type_model(...)`` at first has to construct the UaDataTypeMembers. Therefore the following fields need to be determined.

* *padding*: Already discussed above
* *member_type_index*: Extracted for calculation of the padding as described above
* *namespace_zero*: ``UaBoolean(True)`` since the proposed procedure can only be applied on types from namespace zero (a transfer should be possible)
* *is_array*: The user has to use ``UaList`` in the NamedTuple to indicate that the field is an array. Since ``UaList`` knows its base type class *member_type_index* and *padding* (size of a pointer) can still be inferred
* *is_optional*: Somehow this has to be encoded in the NamedTuple

    * One option is to write some kind of UaDataType interface – let's call this class *UaDataTypeModel* – such that every class representing a custom data type has to implement *UaDataTypeModel*. One could also think of implementing annotations for optional fields.

* *member_name*: Can be inflected from the NamedTuple

Construct the UaDataType
^^^^^^^^^^^^^^^^^^^^^^^^

In a second step our method ``from_data_type_model(...)`` has to build a ``UaDataType`` from those ``UaDataTypeMembers``. Therefore we need the following fields:

* *type_id*: Could be an argument passed to the method and determined by the user (might also be Null and requested from the server)
* *binary_encoding_id*: As well determined by the user (could be passed as a separate argument or encoded via our interface  *UaDataTypeModel* from above)
* *mem_size*: Can be calculated together with the paddings
* *type_index*: Either determined by the user or as the next free index of global list of custom data types
* *type_kind*: This again could be encoded in our in our interface *UaDataTypeModel*

    * Note that the described procedure using NamedTuples applies to structures and structures with optional fields. With some adjustments it could be used for unions as well. It might also be used to represent enums. Nonetheless, this would be counterintuitive since one would expect static fields instead of the instance variables provided by NamedTuple.

* *member_size*: Length of the ``UaList`` with the ``UaDataTypeMembers``
* *type_name*: Can be inflected from the NamedTuple

*Good Luck! :)*


Open issues
------------

Currently there are still a lot of open issues which need to be addressed in order to ensure a satisfying usability and stability of wrappy(o6):

* tests are still very lacking. There are currently only tests for the UaClient and they are not semantically sound. So there is definitely a need for tests for the UaClient, UaServer and UaTypes.
* The current handling of callbacks / function pointers has some major issues / restrictions. A reimplementation or adaptions to improve usability should be considered. Please refer to the :ref:`Callbacks<Callbacks>` for additional information.
* Custom data types are not yet supported. Please find a draft / outline of a possible implementation strategy in the chapter :ref:`Custom Data Types<Custom Data Types>`.
* Historizing is not supported yet
* Pub/sub is not supported yet
* build script has not been tested under systems other than Ubuntu 18.04/20.04
* the documentation needs to be improved to smoothen the experience for new users (e.g. a user guide leading through the provided examples as well as additional example)
* ``UaServer`` (as well as ``UaClient``) are not available as UaTypes with accessible fields (e.g. due to opaque type definitions in open62541).
* ``UaClientConfig`` and ``UaServerConfig`` are still missing some fields for lower level configurations

    * there are functions available in open62541 (open62541/plugins/include/open62541/server_config_default.h) for building a UA_ServerConfig from a basic default config. They easily could be wrapped as methods of ``UaServerConfig`` and as such provide an comfortable way to further customize the server's configurations.

* There is not yet a satisfying solution for double pointers (e.g. ``UA_Variant**``).

    * ``UaList`` could be used for this purpose but should be reworked for a more intuitive and coherent handling

* type handling could further be improved

    * by expanding "type guessing"
    * filling variables of UaTypes could be improved, e.g. via additional __init__ parameters / pseudo constructor methods / builder pattern
    * implicitly applying functions which are explicit in open62541 (see e.g. ``setScalar`` and ``setArray`` handling in UaVariant data setter)
    * struct fields in UA_Types which are supposed to hold arrays should in the wrapping UaType be implemented with UaList type instead of the array's base type. (This should be no problem since ``_value`` of a UaList is the same c type as the lists base type.)
    * by providing a generic deep copy method for UaTypes

