#!/bin/csh
#This script may not work on Edison, Hopper, or Carver.
virtualenv env

source env/bin/activate.csh

pip install -r requirements.txt

git clone  https://bitbucket.org/berkeleylab/qdo.git
pip install -e qdo/py/
pip install -e ../../py/

mkdir ~\.qdo