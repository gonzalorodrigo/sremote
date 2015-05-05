#!/bin/csh
/opt/modules/3.2.10.2/bin/modulecmd tcsh load python
/opt/modules/3.2.10.2/bin/modulecmd tcsh load virtualenv
cd ~/qdo_interpreter
source env/bin/activate
python qdo_remote_server.py "${1}"