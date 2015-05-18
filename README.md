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
- Newt: using NERSC Newt api to access Edison, Hopper, and Carver.

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
Independently of the connector used, these are the steps to execute
a function of a Python module hosted in a remote host.
- Module name, function name and arguments are set in a call request
  object. This object is serialized and copied on a temporary file
  locally.
- The connector is used to copy the request object file to the remote
  host.
- The connector is used to invoke the interpreter.sh in the remote
  host. It receives two input arguments: 
  - The filesystem route where the request object file is located.
  - A filesystem route where the response of the method should be
    stored.
  The local code waits for the interpreter to end.
- interpreter.sh: (in the remote machine)
  - Reads the request object file and deserializes its
    content. The content is interpreted: the module invoked and the
    target functions is called with the indicated input values. The
    return value and standard output of the code is recorded.
  - Constructs a method response object with the return value and
    standard output. Serializes the object and stores it in the
    files ystem at the route pointed as second argument of the
    interpreter.
  - Finishes.
- Once the interpreter has finished, the connector is used to retrieve
  the method response file from the remote host.
- The content is read, deserialized and the return value returned.

Authors
=======

qdo is developed by Gonzalo Rodrigo at Lawrence Berkeley National Lab,
with additional contributions from Stephen Bailey and Shreyas Cholia.  It is
released under the BSD 3-clause open source licence, see LICENSE.
