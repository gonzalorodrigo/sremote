"""
Example of client code to execute the method valid_queue_name
of the QDO module on a remote systems (sremote and qdo
configured). It uses Newt as the communication connector.

Invocation:
python newt.py (edison|hopper|carver) username password
"""
import sremote.api as remote
import sremote.connector.newt as newt
from sys import argv

def valid_queue_name(value):

    # Creation of a connector with Newt capacities,
    connector = newt.ClientNEWTConnector(argv[1])
    # Authentication, this call connects remotely and retrieves the default
    # after login directory.
    connector.auth(argv[2], argv[3])

    # Client class that uses the connector to do the remote calls.
    client = remote.RemoteClient(connector)
    return_value, out = client.do_remote_call("qdo", 
                         "valid_queue_name", args=[value])
    print out
    return return_value


print valid_queue_name("juanito")
print valid_queue_name("juanito!")
