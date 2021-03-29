# Python Wrapper for open62541

This project aims to provide a seamless interface for open62541-functions through the Python interpreter to simplify prototyping without the need for constant recompilation.  

## Prerequisites
Notice: Up until now you'll also need to build open62541 during the build process. Thus make sure you have the required tools (e.g.: `cmake`, `gcc`, ...) installed!

Furthermore, besides the obvious requirement of at least Python3.7, you'll need the following packages, which are best installed through the package manager of your choice:
 
* pip3
* libffi-dev
* libffi6

Additionally through pip3, you need to install:
* cffi
* pdoc
* sphinx_rtd_theme
* flake8
* pytest

## Building

Just `cd` into the project's root directory and run `python3 make.py`. This will currently automatically build open62541, too. See `make.py` for details.


## Usage

For usage information, please refer to our [documentation](https://htmlpreview.github.io/?https://github.com/clge50/open62541-python-wrapper/blob/master/doc/open62541/index.html).
