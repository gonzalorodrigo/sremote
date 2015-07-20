"""Uses SSH connector and connects to a remote host and deploys the SREMOTE
code and an environment for it. It also installs the QDO library in that
environment.

An application using SREMOTE should check is SREMOTE is deployed and use a
similar code to this to deploy it.

It does not require superuser on remote machine. All is installed in the
context of the user.

Usage python do_install_ssh.py full_hostname username password
"""

import sremote.api as remote
import sremote.connector.ssh as ssh
from sys import argv


connector = ssh.ClientSSHConnector(argv[1])
connector.auth(argv[2])

client = remote.RemoteClient(connector)

client.do_bootstrap_install()
 
client.do_install_git_module(
             "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git", 
             "master",
             "qdo")