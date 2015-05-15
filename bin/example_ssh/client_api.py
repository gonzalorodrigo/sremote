"""Resulting remoted module. This is the version of remote_api that is executed
in the client code.It includes the creation of the connector and the the
invocation of the remote classes.
"""


import sremote.api as remote
import sremote.connector.ssh as ssh
from sys import argv


#
# client.do_bootstrap_install()
#
# client.do_install_git_module(
#              "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git")
#
# import sremote.api as remote_api


def valid_queue_name(value):

    connector = ssh.ClientSSHConnector(argv[1])
    connector.auth(argv[2])

    client = remote.RemoteClient(connector)
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", args=[value])
    #print out
    return return_value


print valid_queue_name("juanito")
print valid_queue_name("juanito!")
