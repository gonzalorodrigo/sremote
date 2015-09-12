# SRemote: Simple Remote tool for Python.

## Introduction

SREMOTE stands for Simpler REMOTE: a package to execute Python remotely without
all the usual complications that other packages offer.

The motivation of this library is that most remoting frameworks, although very
complete and powerful require quite some work to setup and deploy. Even more
if the a new connector (element that bring the commands from the local
to the remote host) needs to be re-written (e.g. run over a REST API), using
such libraries can become a nightmare.

**SREMOTE simplifies the model**:it self deploys in the remote host, it
can install libraries and connectors are extremely simple to implement.
** A connector must only support three functions:**

* Execute shell commands in the remote host.

* Push files to the remote host

* Retrieving files from the remote host.
   
## Concepts

In sremote there are Three basic concepts:

- Connector: A connector is a class that offers methods that allow to: copy
files to, retrieve files from, and execute shell commands at a remote machine.

- Endpoint: a set of scripts hosted in the remote machine. They receive the
remote call description from the connector, execute it, and return the result
and stout to the connector.

- RemoteClient: A class that uses a connector to execute python code in the
remote host and returns the corresponding result and stdout.


```
    Local Machine                 Newt Server             Edison
    ========================      ==========    ================================
    |Remote      | NEWT    | ---> | Newt @ | -> | sremote |-> os.getenv("PATH")|
    |Client      |connector|(rest)| NERSC  |    | endpoint|                    |
    ========================      ==========    ================================
                                                                         |
    python type response <------------JSON response----------------------|
```
## Components

### Connectors

The connector has the aforementioned capacities of copying
files to, retrieving files from, and executing shell commands at a remote
machine. The sremote package include two connectors:

- SSH connector: It uses the ssh command. It allows to execute remote python
calls on any host with an ssh server and installed python. For ease of use
it is recommend to use a password-less ssh configuration.

- NEWT Connector: It uses NERSC NEWT REST API to execute commands remotely
on NERSC hosts. It requires a NERSC\_HOST name (e.g. edison), a username, and
password.

The connector is also configured so it can locate the endpoint in the remote
host file system.

### Endpoint

It is composed by a set of scripts that receive the remote call description, 
decode it, and execute it. The endpoint has to be in the remote host before
any Remote Client functions are possible. These scripts are contained in the
res folder of the sremote package.

It also contains a python virtualenv over which other python packages can
be installed to be used by the Remote Client. 

### Remote Client
It uses a connector to execute remote code. It offers the following capacities:
- Deploy the sremote endpoint in the remote host (do\_boot\_strap\_install)
- Install libraries in the configured sremote endpoint (do\_install\_git\_module)
- Execute a method of a python module in the remote machine (do\_remote\_call).
it accepts lists and dicts of arguments.
- Check if a python module is installed in the remote endpoint.
- Set environment variables in the remote host.
- Add path entries to the remote host.

It's initialization only requires an instance of a configured connector.

## Endpoint deployment and configuration
The most critical part of the process is the deployment of the remote endpoint.
There are two possibilities: manual deployment or bootstrap process. 

- Manual deployment: Performed my choosing a remote folder in the remote host
and executing the script bin/deploy\_sremote\_endpoint.sh

- Bootstrap process: The RemoteClient.do\_install\_git\_module reads the
configured sremote\_dir of connector and install the endpoint.

There are two routes that are important for the system: 
- sremote endpoint location: absolute route in the remote file system
containing the endpoint files.
- sremote tmp location: where temporary files or files produced by python
calls will be stored.

There are three ways to configure these locations:

- Default (not configured): sremote\_dir = $HOME/.sremote 
sremote\_tmp = $HOME/.sremote/temp

- Setting folders with *connector.set\_sremote\_dir* and 
*connector.set\_tmp\_dir*. it will use whatever routes are configured there.

- Self discovery: This is a mechanism  triggered  by the method 
*connector.do\_self\_discovery(file\_name)*. It retrieves a file\_name from
$HOME/.sremote. This file contains the routes to sremote dir and tmp dir. In
case the file is not found, it will use pre-existing configuration.
File's content is a JSON dictionary with the following format:
    
    {"sremote": "/tmp/sremote/",
     "absolute_tmp": "/tmp/sremote/tmp"
    }
    (tmp file is set as an absolute route)

    {"sremote": "/tmp/sremote/",
     "absolute_tmp": "sremote_tmp"
    }
    (tmp file is set as an relative route to $HOME:  $HOME/sremote_tmp)

## Examples

### Deployment

The sremote endpoint needs to be deployed in the remote machine. This is
required only once.

SSH connector example.

    import sremote.api as remote
    import sremote.connector.ssh as ssh
    
    connector = ssh.ClientSSHConnector("remote.host.org")
    connector.auth("username")
    client = remote.RemoteClient(connector)
    client.do_bootstrap_install()
    
    #- install a python library from a git repo in the remote endpoint
     client.do_install_git_module(
             "https://bitbucket.org/berkeleylab/qdo.git", 
             "master", "qdo")
    
### Simple remote operation

SSH connector example.

    import sremote.api as remote
    import sremote.connector.ssh as ssh
    
    connector = ssh.ClientSSHConnector("remote.host.org")
    connector.auth("username")
    client = remote.RemoteClient(connector)
    
    #- executes os.makedirs("/tmp/mydir") in the remote host
    client.do_remote_call("os", "makedirs", args=["/tmp/mydir"])

### Self contained
The following examples assume that the sremote endpoint has never been deployed
in the remote machine. In normal use, the deployment only happens once (not just
in this session, but once ever).


SSH connector example. It self-deploys, sets an environ variable and reads it.

    import sremote.api as remote
    import sremote.connector.ssh as ssh
    
    connector = ssh.ClientSSHConnector("remote.host.org")
    connector.auth("username")
    
    client = remote.RemoteClient(connector)
    client.do_bootstrap_install()
    
    #- Previous code is only required to execute once.
    
    #- Sets a remote environment variable. It will be effective while consequent
    #  remote calls are executed. 
    client.register_remote_env_variable("myVar", "myValue")
    
    #- Execute os.getenv("myvar") and retrieve result.
    return_value, out = client.do_remote_call("os", "getenv", 
                                          args=["myVar"]
                                          ) 
    print return_value
        "myValue"
        
        
NERSC connector example. It self-deploys, sets an environ variable and reads it.

    import sremote.api as remote
    import sremote.connector.newt as newt
    
    connector = newt.ClientNEWTConnector("edison")
    connector.auth("username", "password")
    
    client = remote.RemoteClient(connector)
    client.do_bootstrap_install()
    
    #- Previous code is only required to execute once.
    
    #- Sets a remote environment variable. It will be effective while consequent
    #  remote calls are executed.
    client.register_remote_env_variable("myVar", "myValue")
    
    #- Execute os.getenv("myvar") and retrieve result.
    return_value, out = client.do_remote_call("os", "getenv", 
                                          args=["myVar"]
                                          ) 
    print return_value
        "myValue"

More examples can be found in bin/client, bin/installation and the unittests.



## Exceptions raised by do\_remote\_call

if the execution of the python call fails, a number of exceptions are raised.

- ExceptionRemoteExecError: Execution failed remotely. Message indicates
    what. Types of controlled failed: remote module not found, remote method
    not found, method raised exception while executing.
    
- ExceptionRemoteNotSetup: Remote sremote library not present or broken.

## Internals of the Remote Client
Independently of the connector used, these are the steps of do\_remote\_call:

- Module name, function name and arguments are set in a call request
  object. This object is serialized and copied on a temporary file locally.
- The connector is used to copy the request object file to the remote host.
- The connector is used to invoke the endpoint in the remote
  host. It receives two input arguments: 
  - The file system route where the request object file is located.
  - A file system route where the response of the method should be
    stored.
  The local code waits for the interpreter to end.
- The remote endpoint: 
  - Reads the request object file and de-serializes its
    content. The content is interpreted: the module invoked and the
    target functions is called with the indicated input values. The
    return value and standard output of the code is recorded.
  - Constructs a method response object with the return value and
    standard output. Serializes the object and stores it in the
    files system at the route pointed as second argument of the
    interpreter.
  - Finishes.
- Once the interpreter has finished, the connector is used to retrieve
  the method response file from the remote host.
- The content is read, de-serialized and the return value returned.

## Package content
- py/sremote: Core of this system
- bin/deploy\_sremote\_endpoint.sh Configures a sremote endpoint.
- bin/installer: Example code to set up the remote machine tow work Installer:
  it connects to remote host and installs the sremote code. In this
  case they are customized to install the QDO module too.
- bin/client: examples of how to connect a configured remote
  host and execute a function of the qdo library.
- tests: unittest for all the code. Should be used as good examples to write 
code.

Authors
=======
qdo is developed by Gonzalo Rodrigo (gprodrigoalvarez@lbl.gov) at Lawrence
Berkeley National Lab, with additional contributions from Stephen Bailey and Shreyas
Cholia.  It is released under the BSD 3-clause open source license, see LICENSE.
