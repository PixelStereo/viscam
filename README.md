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

Clone the repository and install dependancies
---
    git clone https://github.com/PixelStereo/viscam.git
    cd viscam/
    git submodule update --init
    cd src
    mkdir venv
    cd venv
    pip2 install virtualenv
    virtualenv -p python2 viscam
    cd viscam
    source bin/activate
    pip2 install --upgrade pip
    pip2 install Cython
    cd ../../../3rdparty/pydevicemanager
    pip2 install -r requirements.txt 
    cd ../pyvisca
    pip2 install -r requirements.txt
    pip2 install pyside2
    cd ../../src/

Launch the app
---
    python2 /Users/reno/Documents/GITs/viscam/src/visca_UI.py 

