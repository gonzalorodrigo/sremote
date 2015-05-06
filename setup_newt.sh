#!/bin/csh
set prompt='%B%m%b %C3>'
module load python
module load virtualenv
virtualenv env
source env/bin/activate.csh
pip install -r requirements.txt

git clone https://gonzalorodrigo@bitbucket.org/gonzalorodrigo/qdo_remote_exp.git
cd qdo_remote_exp/py
python setup.py install
mkdir ~\.qdo