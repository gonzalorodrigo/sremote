"""Uses Newt connector and connects to a remote host and deploys the SREMOTE
code and an environment for it. It also installs the QDO library in that
environment.

An application using SREMOTE should check is SREMOTE is deployed and use a
similar code to this to deploy it.

It does not require superuser on remote machine. All is installed in the
context of the user.

Usage: python do_install_newt.py (edison|hopper|carver) username password
"""

import sremote.api as remote
import sremote.connector.newt as newt
from sys import argv

#TODO(gonzalorodrigo): Do better parsing of the input parameters.

connector = newt.ClientNEWTConnector(argv[1])
if not connector.auth(argv[2], argv[3]):
    print "Auth error", argv[2], argv[3]
    exit()

client = remote.RemoteClient(connector)

# Creates remote environment and 
client.do_bootstrap_install()
 
client.do_install_git_module(
             "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git", 
             "master",
             "qdo")