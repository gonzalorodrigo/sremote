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
    #print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

def valid_queue_name_dict(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", 
                                              args={"name":value})
    run_time = time.time()-start_t
    #print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

# Creation of a connector with Newt capacities,
connector = newt.ClientNEWTConnector(argv[1])
#connector.set_tmp_at_home_dir("private_qdo")
#connector.set_sremote_dir("/global/u1/g/gprodri/shared_qdo")
# Authentication, this call connects remotely and retrieves the default
# after login directory.
start_t = time.time()
if connector.auth(argv[2], argv[3]):
    run_time = time.time()-start_t
    print "Auth time (s):", run_time
    # Client class that uses the connector to do the remote calls.
    start_t = time.time()
    connector.do_self_discovery()
    run_time = time.time()-start_t
    print "Self discovery time (s):", run_time
    client = remote.RemoteClient(connector)
    print valid_queue_name("juanito")
    print valid_queue_name_dict("juanito!")
else:
    print "Error in auth!"
