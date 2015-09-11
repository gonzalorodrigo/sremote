#!/bin/bash
#
# This script installs a remote endpoint to be used by sremote at the place where
# it is invoked e.g:
# 
# ~/$ cd folder
# ~/folder/$ ./deploy_sremote_endpoint.sh
#


module load python/2.7.3
module load virtualenv

INSTALL_DIR=`pwd`
TMP_DIR="${INSTALL_DIR}/tmp"
mkdir "${TMP_DIR}"

# First we download what we need.
cd "${TMP_DIR}"
git clone https://github.com/gonzalorodrigo/sremote.git sremote


# installing libraries in the virutal environmeent
cd "${INSTALL_DIR}"
virtualenv env
source env/bin/activate

cd "${TMP_DIR}/sremote/py"
python setup.py install

cd "${INSTALL_DIR}"
echo "Copying files"
cp  "${TMP_DIR}/sremote/py/sremote/res/interpreter.sh" .
cp  "${TMP_DIR}/sremote/py/sremote/res/remote_server.py" .

echo "Setting folder permissions"
chmod o+r .
chmod o+r interpreter.sh  remote_server.py 
chmod -R o=g env
chmod -R o-w .
