#!/bin/bash
set -e
UBUNTU=false
if [ "$(uname)" = "Linux" ]; then
    #LINUX=1
    if type apt-get; then
        OS_ID=$(lsb_release -is)
        if [ "$OS_ID" = "Debian" ]; then
            UBUNTU=false
            echo ""
            echo "WARNING:"
            echo "The Nbzz Blockchain requires a ubuntu 64 bit OS and this is Debain"
            echo "Exiting."
            exit 1
        else
            UBUNTU=true
        fi
    fi
fi

# Check for non 64 bit ARM64/Raspberry Pi installs
if [ "$(uname -m)" = "armv7l" ]; then
    echo ""
    echo "WARNING:"
    echo "The Nbzz Blockchain requires a 64 bit OS and this is 32 bit armv7l"
    echo "Exiting."
    exit 1
fi
# Get submodules
#git submodule update --init mozilla-ca

UBUNTU_PRE_2004=false
if $UBUNTU; then
    LSB_RELEASE=$(lsb_release -rs)
    # In case Ubuntu minimal does not come with bc
    if [ "$(which bc |wc -l)" -eq 0 ]; then sudo apt install bc -y; fi
    # Mint 20.04 repsonds with 20 here so 20 instead of 20.04
    UBUNTU_PRE_2004=$(echo "$LSB_RELEASE<20" | bc)
    UBUNTU_2100=$(echo "$LSB_RELEASE>=21" | bc)
fi

# Manage npm and other install requirements on an OS specific basis
if [ "$(uname)" = "Linux" ]; then
    #LINUX=1
    if [ "$UBUNTU" = "true" ] && [ "$UBUNTU_PRE_2004" = "1" ]; then
        # Ubuntu
        echo "Installing on Ubuntu pre 20.04 LTS."
        sudo apt-get update
        sudo apt-get install -y python3.7-venv python3.7-distutils
        elif [ "$UBUNTU" = "true" ] && [ "$UBUNTU_PRE_2004" = "0" ] && [ "$UBUNTU_2100" = "0" ]; then
        echo "Installing on Ubuntu 20.04 LTS."
        sudo apt-get update
        sudo apt-get install -y python3.8-venv python3-distutils
        elif [ "$UBUNTU" = "true" ] && [ "$UBUNTU_2100" = "1" ]; then
        echo "not support installing on Ubuntu 21.04 or newer."
        echo "Exiting."
        exit 1
    else
        echo "not support."
        echo "Exiting."
        exit 1
    fi
    
else
    echo "not support."
    echo "Exiting."
    exit 1
fi

find_python() {
    set +e
    unset BEST_VERSION
    for V in 37 3.7 38 3.8 39 3.9 3; do
        if which python$V >/dev/null; then
            if [ "$BEST_VERSION" = "" ]; then
                BEST_VERSION=$V
            fi
        fi
    done
    echo $BEST_VERSION
    set -e
}

if [ "$INSTALL_PYTHON_VERSION" = "" ]; then
    INSTALL_PYTHON_VERSION=$(find_python)
fi

# This fancy syntax sets INSTALL_PYTHON_PATH to "python3.7", unless
# INSTALL_PYTHON_VERSION is defined.
# If INSTALL_PYTHON_VERSION equals 3.8, then INSTALL_PYTHON_PATH becomes python3.8

INSTALL_PYTHON_PATH=python${INSTALL_PYTHON_VERSION:-3.7}

echo "Python version is $INSTALL_PYTHON_VERSION"
$INSTALL_PYTHON_PATH -m venv venv
if [ ! -f "activate" ]; then
    ln -s venv/bin/activate .
fi

# shellcheck disable=SC1091
. ./activate
# pip 20.x+ supports Linux binary wheels
python -m pip install --upgrade pip
python -m pip install wheel

python -m pip install -e .

echo ""
echo "Nbzz blockchain install.sh complete."
echo ""
echo "Type '. ./activate' and then 'nbzz init' to begin."