#!/bin/csh
# Endpoint for the NETW remoting.
# It configures the enviroment anda calls the python endpoint.
# 
# Invocation: ./qdo_interpreter_netw.sh (file_route)
#  file_rout: potins to a file containint the request method call object.
set prompt='%B%m%b %C3>' # needed in Carver.
module load python
module load virtualenv
cd ~/qdo_interpreter
source env/bin/activate.csh
python qdo_remote_server.py "${1}"
