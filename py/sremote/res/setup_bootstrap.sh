#!/bin/csh
#
# Script executed to configure a host to execute remote calls for the sremote
# package. This file is deployed on the  remote host at ~/.sremote by the
# sremote bootstrap mechanism.
# 
# It creates the python execution environment in the context of a user in
# a host. It requires python an easy_install to be present and accesible.
#
# The environment cretion implies:
# - Check if pip is present. It not install it
# - Check if virtualenv is present. If not install it.
# - Creacte a python virtual environemnt for the sremote calls.

# Required for Edison, Hopper, and Carver. Will report an error message in other
# systems.


setenv PATH /bin:/usr/bin:/sbin:/usr/sbin:$PATH
if (-f /etc/profile.d/modules.csh) then
	source /etc/profile.d/modules.csh
	module load usg-default-modules
	module load python
	module load virtualenv
endif 

# Locates the binaries to be used.
set python_bin=`which python`
set git_bin=`which git`
set easy_install_bin=`which easy_install`
set virtualenv_bin=`which virtualenv`

set install_dir="$1"
cd $install_dir


which virtualenv
if ($status == 1) then
	echo "Virutalenv is not available, installing"
	mkdir pythonuserbase
	setenv PYTHONUSERBASE "./pythonuserbase"
	mkdir -p "$PYTHONUSERBASE/lib/python/site-packages"
	mkdir -p "$PYTHONUSERBASE/bin"
	$easy_install_bin --user pip
	set pip_bin="$PYTHONUSERBASE/bin/pip"


	$pip_bin install --user virtualenv
	set virtualenv_bin="$PYTHONUSERBASE/bin/virtualenv"
endif

$virtualenv_bin env
