""" 
Tool-box to do remote Python functions calls.

The class RemoteClient and RemoteServer use these methods to serialize and
deserialize the method call request and the method response.

The method call request is a dictionary with two items:
    - dic[COMMAND_TYPE]: string with  of the method to be executed
    - dic[COMMAND_ARGS]: list of arguments of the method to be executed.
e.g. call for methods
    foo(arg1, arg2)
    {COMMAND_TYPE: "foo", COMMAND_ARGS: [val_arg1, val_arg2]}

The method response is a dictionary with two times:
    - dic[RESPONSE_STATUS]: bool, True if the remote method call got to end.
    - dic[RESPONSE_CONTENT]: if status == True then the return value of the
      remote call. If status == False then a string explaining what failed. 
 
 This methods uses JSON as a serializer, it can be changed by using
 set_serializer

"""
import json

COMMAND_MODULE = "module"
COMMAND_TYPE = "command"
COMMAND_ARGS = "args"
RESPONSE_STATUS = "success"
RESPONSE_CONTENT = "return_value"

_serializer = json

def call_method_object_command(call_request):
    """Executes method in obj as instructed  by call_request.
    
    Args:
        obj: object whose method will be executed.
        call_request: method call request. It indicates the name of the method
        to be called and the argument values to be pased.
    
    Returns:
        whatever the called method in obj returns.    
    """
    module_name = call_request[COMMAND_MODULE]
    command_name = call_request[COMMAND_TYPE]
    args_obj = call_request[COMMAND_ARGS]
    return call_method_object(module_name, command_name, args_obj)

def call_method_object(module_name, method_name, args):
    """Executes obj.method_name(*args) and returns what ever it returns."""
    obj = __import__(module_name, fromlist=[''])
    print obj
    method = getattr(obj, method_name)
    output = method(*args)
    return output

def process_remote_call(request_string):
    """Deserializes a call_request and executes it in invoked_object.
    
    Args:
        invoked_object: object whose method will be executed.
        request_string: call_request in serialized format.
    Returns: 
        result of executing whatever is specified in request_sting in
        invoked_object.
    """ 
    module_name, method_name, args = decode_call_request(request_string)
    return call_method_object(module_name, method_name, args)

def encode_call_request(module_name, command_name, args = []):
    """Creates a call_request_object and serializes it."""
    command_obj = {COMMAND_TYPE: command_name}
    command_obj[COMMAND_ARGS] = args
    command_obj[COMMAND_MODULE] = module_name
    return serialize_obj(command_obj)
    
def decode_call_request(call_request_serialized):
    """Deserializes and decodes a call_request_object."""
    obj = deserialize_obj(call_request_serialized)
    return obj[COMMAND_MODULE], obj[COMMAND_TYPE], obj[COMMAND_ARGS]
    
def encode_call_response(return_value, success=True):
    """Encodes and serializes a method response."""
    response = {RESPONSE_STATUS:success}
    response[RESPONSE_CONTENT] = return_value
    return serialize_obj(response)

def decode_call_response(call_response_serialized):
    """Deserializes and decodes a method response."""
    try:
        response_obj = deserialize_obj(call_response_serialized)
        return response_obj[RESPONSE_STATUS], response_obj[RESPONSE_CONTENT]
    except:
        return False, "Bad response: "+str(call_response_serialized)
 
def set_serializer(serializer):
    """Sets the serializer of the library.
    
    Args:
        serializer: an object that implements the methods:
            - dumps(obj): returns the serialized vesio of obj
            - loads(serialized_obj): returns the object serialized in
              seriazlied_obj. 
    """
    _serializer = serializer

def serialize_obj(obj):
    """return serialized version of obj."""
    return _serializer.dumps(obj)
   
def deserialize_obj(command_string):
    """returns object serialized in command_string."""
    return _serializer.loads(command_string)



