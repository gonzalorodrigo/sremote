"""Example of client code to execute the method valid_queue_name
of the QDO module on a remote systems (sremote and qdo
configured). It uses Newt as the communication connector.

Invocation:
python newt.py (edison|hopper|carver) username password
"""
import sremote.api as remote
import sremote.connector.newt as newt
import time
from sys import argv

def valid_queue_name(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", 
                         "valid_queue_name", args=[value])
    run_time = time.time()-start_t
    print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

def valid_queue_name_dict(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", 
                                              args={"name":value})
    run_time = time.time()-start_t
    print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

# Creation of a connector with Newt capacities,
connector = newt.ClientNEWTConnector(argv[1])
# Authentication, this call connects remotely and retrieves the default
# after login directory.
if connector.auth(argv[2], argv[3]):
    # Client class that uses the connector to do the remote calls.
    client = remote.RemoteClient(connector)
    print valid_queue_name("juanito")
    print valid_queue_name_dict("juanito!")
else:
    print "Error in auth!"
