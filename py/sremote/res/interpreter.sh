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
if (-f /etc/profile.d/modules.csh) then
	source /etc/profile.d/modules.csh
	module load usg-default-modules
	module load python
	module load virtualenv
endif 

#module load python
if ( "${3}" == "") then
	set install_dir="~/.sremote"
else
	set install_dir="${3}"
endif

if ( "${4}" != "") then
	mkdir -p "${4}/tmp"
endif

cd $install_dir
source env/bin/activate.csh

#- enables QDO (if called) to disable its virtualenvironment
setenv _OLD_VIRTUAL_PATH $_OLD_VIRTUAL_PATH
setenv QDO_VIRTUAL_DEACTIVATE "do"

set python_bin=`which python`

if ( "${4}" != "") then
	mkdir -p "${4}"
	cd "${4}"
endif
python "${install_dir}/remote_server.py" "${1}" "${2}"
