#!/bin/csh
#
# Retrieves a python module from a git repository, selects
# the desired branch and installs it in the sremote environment.
# Requires git and the sremote environment. This file is deployed on the
# remote host by the sremote bootstrap mechanism.
#
# Usage: ./install_git_module.sh repository_url [branch]
# - repository_url: https url towards the repo. e.g. 
#   https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git
# - branch: if not set, the master branch is installed. If set, the selected
#   one is.

setenv PATH /bin:/usr/bin:/sbin:/usr/sbin:$PATH
if (-f /etc/profile.d/modules.csh) then
	source /etc/profile.d/modules.csh 
	module load usg-default-modules
	module load python
	module load virtualenv
endif 


set python_bin=`which python`
set git_bin=`which git`
set easy_install_bin=`which easy_install`
set install_dir="~/.sremote"
cd $install_dir
source env/bin/activate.csh

#TODO(gonzalorodrigo): More robust argument parsing.

mkdir tmp
cd tmp
$git_bin clone $1 module_source

cd module_source
if ($#argv == 2) then
	$git_bin checkout $2 
endif
cd py
python setup.py install
cd ../..

if (-d module_source ) then
	echo "Cleaning up"
    rm -rf module_source
endif