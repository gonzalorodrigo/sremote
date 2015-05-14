"""python Endpoint for QDO

    Args:
        argv[1]: files system route pointing to a file containing the method
        call request.
    
    Std_out: serialized version of the return object summarizing the execution
    of the method to be called.
"""


import sremote.api
import sys

class ServerNewtConnector(sremote.api.ServerChannel):   
    def retrieve_call_request(self, method_request_reference):
        text_file = open(method_request_reference, "r")
        content = "\n".join(text_file.readlines())
       
        return content


conn =  ServerNewtConnector()
if (sys.argv):
    file_route = sys.argv[1]

    print conn.process_call_request(file_route)
else:
    print conn.return_error()