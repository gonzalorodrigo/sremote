"""python Endpoint for the local connector

    Args:
        argv[1]: files system route pointing to a file containing the method
        call request.
    
    Std_out: serialized version of the return object summarizing the execution
    of the method to be called.
"""

import sremote.connector.ssh as ssh
import sys

conn =  ssh.ServerSSHConnector()
if (sys.argv):
    file_route = sys.argv[1]
    out_file_route = sys.argv[2]
    print conn.process_call_request(file_route, out_file_route)
else:
    print conn.return_error()