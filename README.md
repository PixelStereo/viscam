# viscam
Python Crossplatform Application to control Camera through VISCA protocol

Only for Python 2 for the moment.


Install Python and create a virtual environment
---
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew update
    brew upgrade
    brew install python2
    brew install liblo
    brew install git

Clone the repository and install dependancies
---
    git clone https://github.com/PixelStereo/viscam.git
    cd viscam/
    git submodule update --init
    cd src
    mkdir venv
    cd venv
    pip2 install virtualenv
    python2 -m virtualenv -p python2 viscam
    cd viscam
    source bin/activate
    pip2 install --upgrade pip
    pip2 install Cython
    cd ../../../3rdparty/pydevicemanager
    pip2 install -r requirements.txt 
    pip2 install -ve .
    cd ../pyvisca
    pip2 install -r requirements.txt
    pip2 install -ve .
    pip2 install pyside2
    cd ../../src/

Launch the app
---
    python2 main.py


If you had some errors with pyliblo, you can install it by hand

    cd venv/viscam/lib/python2.7/site-packages/
    wget http://das.nasophon.de/download/pyliblo-0.10.0.tar.gz
    tar -xjvf pyliblo-0.10.0.tar.gz
    cd pyliblo-0.10.0
    C_INCLUDE_PATH=/usr/local/include LIBRARY_PATH=/usr/local/lib python2 setup.py install
    cd ../../../
    cd ../../..
    python2 /Users/reno/Documents/GITs/viscam/src/viscam.py 
