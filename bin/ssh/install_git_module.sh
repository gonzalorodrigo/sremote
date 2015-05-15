#!/bin/csh
#This script may not work on Edison, Hopper, or Carver.
module load python
module load virtualenv

set python_bin=`which python`
set git_bin=`which git`
set easy_install_bin=`which easy_install`
set install_dir="~/.sremote"
cd $install_dir
source env/bin/activate.csh

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