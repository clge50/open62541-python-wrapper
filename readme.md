# wrappy(o6): A Python wrapper for open62541

The wrappy(o6) project aims to provide a seamless interface for open62541-functions through the Python interpreter to simplify prototyping without the need for constant recompilation.  


## Prerequisites
Testing has so far only been done on Ubuntu 18.04 and Ubuntu 20.04., but building on other GNU/Linux systems should also work. Windows and Mac OS are currently not officially supported!
### wrappy(o6)
Notice: Up until now you'll also need to build open62541 during the build process. Thus make sure you have the [required tools](https://open62541.org/doc/current/building.html) (e.g.: `cmake`) installed!

Furthermore, you'll need the following packages, which are best installed through the package manager of your choice:
 
* python3
* pip3
* libffi
* libffi-dev

Additionally, using `pip3`, you need to install:
* cffi


### Documentation
The full documentation is available offline and can be built separately. This process is entirely optional.\
In order to build the documentation, you also need:
* python3-sphinx
  
And via `pip3`:
* sphinx_rtd_theme


## Building

Just `cd` into the project's root directory and run `python3 make.py`. This will currently automatically build open62541, too. See `make.py` for details.

To build the documentation, also run `python3 make_sphinx.py`. Please make sure to have the optional dependencies given above installed.

## Usage

Notice: Since wrappy(o6) is still in an early stage of development, some features are not yet considered stable. Also, some features of open62541 (e.g. Historizing, PubSub) are still missing.   

For usage information, please refer to our [documentation](https://github.com/clge50/open62541-python-wrapper/tree/master/sphinx/build/html/index.html).
