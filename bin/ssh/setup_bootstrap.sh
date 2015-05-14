#!/bin/csh
#This script may not work on Edison, Hopper, or Carver.
module load python
module load virtualenv

set python_bin=`which python`
set git_bin=`which git`
set easy_install_bin=`which easy_install`
set virtualenv_bin=`which virtualenv`
set install_dir="~/.sremote/ssh"
cd $install_dir

echo "Checking if virutalenv is available"
which virtualenv
if ( $1 == 1) then
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

# source env/bin/activate.csh

# set python_bin=`which python`
# echo "Using python: ${python_bin}"
# #pip install -r requirements.txt

# if (-d remote_libs_repo ) then
# 	echo "Cleaning up previous copy of remote lib"
#     rm -rf remote_libs_repo
# endif

# $git_bin clone https://github.com/gonzalorodrigo/qdo_interpreter.git remote_libs_repo
# cd remote_libs_repo
# $git_bin checkout modular
# cd py
# ${python_bin} setup.py install