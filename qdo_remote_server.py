"""python Endpoint for QDO

    Args:
        argv[1]: files system route pointing to a file containing the method
        call request.
    
    Std_out: serialized version of the return object summarizing the execution
    of the method to be called.
"""

import qdo
import qdo_remote_api_sim
import sys

conn = qdo_remote_api_sim.QDOLocalConnector()
if (sys.argv):
    file_route = sys.argv[1]

    print conn.process_call_request(qdo, file_route)
else:
    print conn.return_error()