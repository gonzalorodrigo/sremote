#!/bin/bash
cd ~/qdo_interpreter
source env/bin/activate
python qdo_remote_server.py "${1}"