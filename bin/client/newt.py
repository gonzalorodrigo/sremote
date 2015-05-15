
import sremote.api as remote
import sremote.connector.newt as newt
from sys import argv


#
# client.do_bootstrap_install()
#
# client.do_install_git_module(
#              "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git")
#
# import sremote.api as remote_api


def valid_queue_name(value):

    connector = newt.ClientNEWTConnector(argv[1])
    connector.auth(argv[2], argv[3])

    client = remote.RemoteClient(connector)
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", args=[value])
    #print out
    return return_value


print valid_queue_name("juanito")
print valid_queue_name("juanito!")
