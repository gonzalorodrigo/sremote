#!/bin/csh
module load python
module load virtualenv
virtualenv env
source env/bin/activate.csh
pip install -r requirements.txt