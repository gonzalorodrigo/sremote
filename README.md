## SRemote: Simple Remote tool for Python.

### Introduction
This code is meant to enable remote execution of Python code. It is
composed of:
- bin/installer: Code to set up the remote machine tow work Installer:
  it connects to remote host and installs the sremote code. In this
  case they are customized to install the QDO lib also.
- bin/client: Two examples of how to connect a configured remote
  host and execute a fuction of the qdo library.
- sremote package: Core of this system. Includes the general functions
  for deployment, remote execution and the connectors. The connectors
  are specific class that allow control of the remote host with
  the following minimum functions:copy a file to the remote host,
  read a file from the remote host, and execute code in it. 
  
There are two implementations of the connectors:
- SSH: using ssh execution and scp.
- Newt: using NERSC newt api to access Edison, Hopper, and Carver.

### Instalation
The installation process sets up the a user account of the remote
host:
- Creates .sremote folder in 
- It enables Python.
- Installs pip and virtualenv localy (only if not present).
- Creates a virtual environment.
- Retrieves this the sremote lib from a git repo and installs it
  in the environment.
- Retrieves the QDO library from a git repo and installs it in the
  environment.
 
Code using remote calls only have to use calls like the ones
present in the bin/client code files. 

### Communication protocol