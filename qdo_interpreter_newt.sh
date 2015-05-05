#!/bin/bash
source env/bin/activate
cd ~/qdo_interpreter
python qdo_remote_server.py "${1}"