i#!/bin/bash
source env/bin/activate.csh
cd ~/qdo_interpreter
python qdo_remote_server.py "${1}"