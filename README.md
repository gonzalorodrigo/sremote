### qdo_interpreter

This code is meant to enable remoting of python code through NEWT: code
calls a ptyhon method in a host, but it is actually executed in a NERSC system.
It only allows to remote methods which arguments and return are serializable
by JSON.

To see how it works:
- Clone this repo somewhere.
- run setup_sim.sh: it creates the environment to run the simulated version
(communacation end point through local files) and retrieves a modified version
of the QDO library with a special method: qsummary, generates a JSON
summary of the queues,
- run python test_qdo_remote_newt.py to see how it works.


Test the NEWT version:
NERSC side:
- Login in a NERSC side
- Clone the repo in your home directory.
- run setup_newt.sh: it creates the environment to run the NEWT version
 and retrieves a modified version of the QDO library with a special method:
 qsummary, generates a JSON
 summary of the queues,

CLient side:
- Clone the repo in your home directory.
- run setup_newt.sh. Some things will give error messages but it is fine.
- run: python test_qdo_remote_sim.py "username" "password"
(use your NERSC user pass)

### Code Generator




