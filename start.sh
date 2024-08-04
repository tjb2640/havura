#!/bin/sh

ENVDIR="./env"
PYCMD="python3"
PIPCMD="pip3"

# Virtualenv
if ! [ -d "$ENVDIR" ]; then
    printf "Creating a venv for Havura to run in\\n"
    $PYCMD -m venv "$ENVDIR"
fi
source $ENVDIR/bin/activate


# Dependency checks
function dhandle () {
    $PYCMD -m pip show "$1" 1>/dev/null 2>/dev/null
    if [ $? -eq 1 ]; then
        printf "Installing pip dependency '$1'...\\n"
        $PYCMD -m pip install "$1"
    fi

    if [ $? -eq 1 ]; then
        printf "  Could not resolve needed depencency '$1' :(\\n"
        exit 1
    fi
}

dhandle "blessed" # terminal apps helper library
dhandle "requests"
dhandle "jsonpickle"

$PYCMD src/main.py
printf "Havura is exiting.\\n"
