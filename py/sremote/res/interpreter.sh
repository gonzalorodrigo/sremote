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

setenv PATH /bin:/usr/bin:/sbin:/usr/sbin:$PATH

#module load python
if ( "${3}" == "") then
	set install_dir="~/.sremote"
else
	set install_dir="${3}"
endif

if ( "${4}" != "") then
	mkdir -p "${4}/tmp"
endif

if ( "${5}" != "") then
	mkdir -p "${5}"

cd $install_dir

if ( -f "virtualenvs/py2.7/bin/activate.csh" ) then
	source virtualenvs/py2.7/bin/activate.csh
else
	if (-f /etc/profile.d/modules.csh) then
		source /etc/profile.d/modules.csh
		module load usg-default-modules
		module load python
		module load virtualenv
	endif 
	source env/bin/activate.csh
endif


set python_bin=`which python`

if ( "${5}" != "") then
	cd "${5}"
endif

# -E makes python ignore all the environemnt variables that point to libraries
# that may conflict with the installed in the virtual environment.
$python_bin -E "${install_dir}/remote_server.py" "${1}" "${2}"
