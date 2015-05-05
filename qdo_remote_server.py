import qdo
import remote_server
import sys

if (sys.argv):
    file_route = sys.argv[1]
    print remote_server.process_incomming_call(qdo, file_route)
else:
    print remote_server.return_error()