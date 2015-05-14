#!/bin/bash
module load python
module load virtualenv

source env/bin/activate
set python_bin=`which python`
cd ~/.sremote
setenv PYTHONUSERBASE "./pythonuserbase"
python remote_server.py "${1}"