"""Example of client code to execute the method valid_queue_name
of the QDO module on a remote systems (sremote and qdo
configured). It uses SSH as the communication connector.

Invocation:
python newt.py full_hostname username password
"""

import sremote.api as remote
import sremote.connector.ssh as ssh
import time
from sys import argv


def valid_queue_name(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", args=[value])
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

#
# client.do_bootstrap_install()
#
# client.do_install_git_module(
#              "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git")
#
# import sremote.api as remote_api
connector = ssh.ClientSSHConnector(argv[1])
connector.auth(argv[2])

client = remote.RemoteClient(connector)




print valid_queue_name("juanito")
print valid_queue_name_dict("juanito!")
