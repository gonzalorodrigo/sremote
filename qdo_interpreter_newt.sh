#!/bin/bash
module load python
module load virtualenv
cd ~/qdo_interpreter
source env/bin/activate
python qdo_remote_server.py "${1}"