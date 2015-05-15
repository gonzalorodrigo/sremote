#!/bin/csh
module load python
module load virtualenv
set install_dir="~/.sremote"
cd $install_dir
source env/bin/activate.csh
set python_bin=`which python`

python remote_server.py "${1}" "${2}"
