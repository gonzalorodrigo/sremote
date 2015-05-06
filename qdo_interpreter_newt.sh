#!/bin/csh
set prompt='%B%m%b %C3>'
module load python
module load virtualenv
cd ~/qdo_interpreter
source env/bin/activate.csh
python qdo_remote_server.py "${1}"
