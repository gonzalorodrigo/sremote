"""python Endpoint for QDO

    Args:
        argv[1]: files system route pointing to a file containing the method
        call request.
    
    Std_out: serialized version of the return object summarizing the execution
    of the method to be called.
"""


import newt_connector
import sys

conn = newt_connector.NewtConnector()
if (sys.argv):
    file_route = sys.argv[1]

    print conn.process_call_request(file_route)
else:
    print conn.return_error()