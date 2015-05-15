"""
Example of client code to execute the method valid_queue_name
of the QDO module on a remote systems (sremote and qdo
configured). It uses Newt as the communication connector.

Invocation:
python newt.py (edison,hopper,carver) username pass
"""
import sremote.api as remote
import sremote.connector.newt as newt
from sys import argv

def valid_queue_name(value):

    connector = newt.ClientNEWTConnector(argv[1])
    connector.auth(argv[2], argv[3])

    client = remote.RemoteClient(connector)
    return_value, out = client.do_remote_call("qdo", 
                         "valid_queue_name", args=[value])
    print out
    return return_value


print valid_queue_name("juanito")
print valid_queue_name("juanito!")
