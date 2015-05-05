from xml_marshaller import xml_marshaller

COMMAND_TYPE = "command"
COMMAND_ARGS = "args"
RESPONSE_STATUS = "success"
RESPONSE_CONTENT = "return_value"

def call_method_object_command(obj, command_obj):
    print command_obj
    command_name = command_obj[COMMAND_TYPE]
    args_obj = command_obj[COMMAND_ARGS]
    return call_method_object(command_name, args_obj)

def call_method_object(obj, name, args):
    method = getattr(obj, name)
    output = method(*args)
    return output

def process_remote_call(remote_obj, command_string):
    command, args = decode_commnad(command_string)
    call_method_object(remote_obj, command, args)

def encode_command(command, args = []):
    command_obj = {COMMAND_TYPE: command}
    command_obj[COMMAND_ARGS] = args
    return serialize_obj(command_obj)
    
def decode_commnad(command_string):
    obj = deserialize_obj(command_string)
    return obj[COMMAND_TYPE], obj[COMMAND_ARGS]
    
def encode_response(obj, success=True):
    response = {RESPONSE_STATUS:success}
    response[RESPONSE_CONTENT] = obj
    return serialize_obj(response)

def decode_response(response_string):
    response_obj = deserialize_obj(response_string)
    return response_obj[RESPONSE_STATUS], response_obj[RESPONSE_CONTENT]
 
 
def serialize_obj(obj):
    return xml_marshaller.dumps(obj)
   
def deserialize_obj(command_string):
    return xml_marshaller.loads(command_string)

