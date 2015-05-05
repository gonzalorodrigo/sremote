
import sys
import remote_api as remote

def process_incomming_call(target_obj, method_call_request_route):
    text_file = open(method_call_request_route, "r")
    content = "\n".join(text_file.readlines())
    command_name, args = remote.decode_call_request(content)
    reponse_obj = remote.call_method_object(target_obj, command_name, args)
    return remote.encode_call_response(reponse_obj, True)
    
def return_error():
    return remote.encode_call_response({}, False)
    
    
