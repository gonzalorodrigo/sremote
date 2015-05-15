"""Start point of the server side code of the smremote. Invoked my the
interpreter.

Args:
    argv[1]: files system route pointing to a file containing the method
    call request.
    argv[2]: files system route pointing  where the request response
    shoudl be written to.

Std_out: serialized version of the return object summarizing the execution
of the method to be called.
"""

import sremote.api as remote
import sys

conn =  remote.ServerChannel()
if (sys.argv):
    file_route = sys.argv[1]
    out_file_route = sys.argv[2]
    print conn.process_call_request(file_route, out_file_route)
else:
    print conn.return_error()