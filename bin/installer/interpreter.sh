#!/bin/csh
#
# Entry point for the remote calls in the sremote package. It sets the required
# environemnt for sremote and invokes the code that will parse the request,
# execute the requested function, and produce the repsonse. This file is 
#deployed on the remote host at ~/.sremote by the sremote bootstrap mechanism.
#
# Usage: ./interpreter request_route response_route
# - request_route: file system route pointing to a file containing a serialized
#   function call request.
# - resposne_route: file system route to be used by sremote to write the 
#   result of the execution of the function call request.

# For Edison, Hopper, and Carver.
module load python
module load virtualenv

set install_dir="~/.sremote"
cd $install_dir
source env/bin/activate.csh
set python_bin=`which python`

python remote_server.py "${1}" "${2}"
