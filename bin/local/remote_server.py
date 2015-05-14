"""python Endpoint for the local connector

    Args:
        argv[1]: files system route pointing to a file containing the method
        call request.
    
    Std_out: serialized version of the return object summarizing the execution
    of the method to be called.
"""

import local_connector
import sys

conn =  local_connector.ServerLocalConnector()
if (sys.argv):
    file_route = sys.argv[1]
    print conn.process_call_request(file_route)
else:
    print conn.return_error()