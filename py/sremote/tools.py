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
import os
import types
from __builtin__ import False

COMMAND_MODULE = "module"
COMMAND_TYPE = "command"
COMMAND_ARGS = "args"
COMMAND_MODULES_CHECK = "modules_check"
COMMAND_ENV_VARIABLES = "enviroment_variables"
COMMAND_COND_ENV_VARIABLES = "conditional_enviroment_variables"
COMMAND_PATH_ADDONS = "path_addons"


RESPONSE_STATUS = "success"
RESPONSE_CONTENT = "return_value"
RESPONSE_VERSION = "sremote_version"
RESPONSE_MODULES_CHECK = "modules_check"

_serializer = json

class ExceptionRemoteExecError(Exception):
    def get_serialized(self):
        return dict(sremote_type="ExceptionRemoteExecError",
                    message = str(self))

class ExceptionRemoteNotSetup(Exception):
    pass

class ExceptionRemoteModulesError(Exception):
    pass

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

    if not module_exists(module_name):
        raise ExceptionRemoteExecError("Module "+ module_name +
                                       " could not be imported")
    obj = __import__(module_name, fromlist=[''])
    #print obj
    if not hasattr(obj, method_name):
        raise ExceptionRemoteExecError("Method " + method_name +
                                       " not present in" +
                                       " module "+module_name)
    method = getattr(obj, method_name)
    if isinstance(args, types.ListType):
        try:
            output = method(*args)
        except Exception as e:
            raise ExceptionRemoteExecError("Method " + method_name + " raised "
                                           "exception. Args(" + str(args) +
                                           "). Exception: " + str(e))
    elif isinstance(args, types.DictType):
        try:
            output = method(**args)
        except Exception as e:
            raise ExceptionRemoteExecError("Method "+method_name+" raised "
                                           "exception. Args("+str(args) +
                                           "). Exception: " + str(e))
    else:
        raise ExceptionRemoteExecError("Wrong arguments type for method: " +
                                       str(args))
    return output

def set_environ_variables(dic_variables, only_if_not_set=False):
    for (name, value) in dic_variables.iteritems():
        if only_if_not_set and os.getenv(name)!=None:
            continue
        os.environ[name]=value

def add_environ_path(path_list):
    if path_list:
        old_path = os.getenv("PATH")
        for path in path_list:
            old_path+=":"+path
        os.environ["PATH"]=old_path

def process_remote_call(request_string):
    """Deserializes a call_request and executes it in invoked_object.
    
    Args:
        invoked_object: object whose method will be executed.
        request_string: call_request in serialized format.
    Returns: 
        result of executing whatever is specified in request_sting in
        invoked_object.
    """ 
    module_name, method_name, args, modules_check, env_variables, \
        cond_env_variables, path_addons= \
                 decode_call_request(request_string)
    for mod in modules_check:
        if not module_exists(mod):
            raise ExceptionRemoteExecError("Module "+ module_name +
                                           " could not be imported")
    set_environ_variables(env_variables)
    set_environ_variables(cond_env_variables, True)
    add_environ_path(path_addons)
    return call_method_object(module_name, method_name, args)

def encode_call_request(module_name, command_name, args = [], 
                        required_extra_modules = [],
                        remote_env_variables = {},
                        conditional_remote_env_variables = {},
                        remote_path_addons = []):
    """Creates a call_request_object and serializes it."""
    all_modules = required_extra_modules
    command_obj = {COMMAND_TYPE: command_name}
    command_obj[COMMAND_ARGS] = args
    command_obj[COMMAND_MODULE] = module_name
    command_obj[COMMAND_MODULES_CHECK] = all_modules
    command_obj[COMMAND_ENV_VARIABLES] = remote_env_variables
    command_obj[COMMAND_COND_ENV_VARIABLES] = conditional_remote_env_variables
    command_obj[COMMAND_PATH_ADDONS] = remote_path_addons
    return serialize_obj(command_obj)
    
def decode_call_request(call_request_serialized):
    """Deserializes and decodes a call_request_object."""
    obj = deserialize_obj(call_request_serialized)
    return obj[COMMAND_MODULE], obj[COMMAND_TYPE], obj[COMMAND_ARGS], \
        obj[COMMAND_MODULES_CHECK], obj[COMMAND_ENV_VARIABLES], \
        obj[COMMAND_COND_ENV_VARIABLES], obj[COMMAND_PATH_ADDONS]
    
def encode_call_response(return_value, success=True,
                         required_extra_modules=[]):
    """Encodes and serializes a method response."""
    response = {RESPONSE_STATUS:success}
    response[RESPONSE_CONTENT] = return_value
    response[RESPONSE_VERSION] = get_sremote_version()
    response[RESPONSE_MODULES_CHECK] = \
            get_modules_versions(required_extra_modules)
    
    return serialize_obj(response)

def decode_call_response(call_response_serialized):
    """Deserializes and decodes a method response."""
    try:
        response_obj = deserialize_obj(call_response_serialized)
        #print response_obj
    except:
        return False, "Bad response: "+str(call_response_serialized)
    version = get_sremote_version()
    if not RESPONSE_VERSION in response_obj.keys():
        raise ExceptionRemoteNotSetup("SREMOTE Version info not present in"+
                                      " response")
    if response_obj[RESPONSE_VERSION] != version:
        raise ExceptionRemoteNotSetup("SREMOTE version miss-match: remote("
                                      + str(response_obj[RESPONSE_VERSION])
                                      +") != local("+str(version)
                                      +")")
        
    if not RESPONSE_MODULES_CHECK in response_obj.keys():
        raise ExceptionRemoteNotSetup("Modules check version info not present in"+
                                      " response")
    check_modules_versions(response_obj[RESPONSE_MODULES_CHECK])
    return response_obj[RESPONSE_STATUS], response_obj[RESPONSE_CONTENT]
   
 
def set_serializer(serializer):
    """Sets the serializer of the library.
    
    Args:
        serializer: an object that implements the methods:
            - dumps(obj): returns the serialized obj
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

def module_exists(module_name):
    """returns True if module can be imported"""
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
import pkg_resources

def get_sremote_version():
    """returns the version stated in the setup.py of sremote package"""
    return get_module_version("sremote")

def get_modules_versions(modules_name_list):
    module_versions = {}
    for module_name in modules_name_list:
        version = None
        if module_exists(module_name):
            version = get_module_version(module_name)
        module_versions[module_name] = version
    return module_versions
    
def get_module_version(module_name):
    return pkg_resources.get_distribution(module_name).version

def check_modules_versions(module_dic):
    """Checks a dictionary of module_name:version against the ones installed
    in the execution environment. It checks all the modules and raises an
    exeception at the end. Conditions for exception for each module:
    - Module not present in execution environment.
    - Module version is none (note present in remote environment.
    - Module versions miss-match.
    """ 
    msj = ""
    all_modules_ok=True
    for (name, version) in module_dic.iteritems():
        if not module_exists(name):
            all_modules_ok=False
            msj+="Module "+name+" not present in local machine.\n"
        elif version == None:
            all_modules_ok = False
            msj+="Module "+name+" nor present in remote machine.\n"
        elif version!=get_module_version(name):
            all_modules_ok=False
            msj+=("Module "+name+" version miss-match: local(" + 
                str(get_module_version(name)) + ")-remote("+
                str(version))+")"
    if not all_modules_ok:
        raise(ExceptionRemoteModulesError(msj))

def parse_location_file(text):
    """Decodes a JSON object from a string into a dictionary. This object
    represents the configuration of the sremote library.
    Args:
        text: string containing a serialized json object. This object has the
            following requirements:
                - srmote: (required) containing a string pointing to a remote 
                  filesystem location for the sremote endpoint.
                - relative_tmp: containing a string pointing to a remote 
                  filesystem location for the sremote tmp. This location is
                  relative to the user's home directory.
                - absolute_tmp: containing a string pointing to a remote 
                  filesystem location for the sremote tmp. This location is
                  an absolute route.
            Either one of relative_tmp or absolute_tmp has to be set.
    Returns: a dictionary with the json object content. Returns false if the
        text cannot be deserialized of fields are missing.
    """
    try:
        obj = json.loads(text)
    except Exception as e:
        return False
    print obj
    if "sremote" in obj.keys():
        if ((not "relative_tmp" in obj.keys()) and 
            (not "absolute_tmp" in obj.keys())):
            return False
    return obj
    

