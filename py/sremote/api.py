""" 
Classes to do remote Python functions calls in sremote.

This code allows to call remote functions of methods that receive and return
serializable objects. 

"""
import datetime
import os
from pkgutil import get_loader
import sremote.tools as remote
import sys
import types
import uuid
from __builtin__ import str

class RemoteClient(object):
    """Base class for the client side of the remoting functions including:
    - Deployment of the the sremote environment in the remote host.
    - Installation of the sremote library in the remote hosts's environemnt.
    - Installation of python modules in the remote hotst's sremote environment.
    - Call from the client side to execute a method remotely.

    During creation it receives a ClientChannel object includes the information
    about the remote host and a communication protocol.
    """

    def __init__(self, comms_client):
        """Init of the class

        Args:
            comms_client: an object that is super class of RemoteComms class.
        """
        self._comms_client = comms_client
        self._registered_remote_modules = []
        self._remote_env_variables = {}
        self._conditional_remote_env_variables = {}

    def do_remote_call(self, module_name, method_name, args=[], keep_env=False):
        """Uses _comms_client to send a request to execute
        module_name.method_name(*args) in the remote host. It asumes that
        module_name is installed in the sremote environemnt of the remote 
        host.

        Args:
            module_name: string with the name of the module which method will be
                executed.
            method_name: string with name of the method to be executed.
            args: list or dict containing the argument values. Dict is desired
                for calling methods with default values.
            keep_env: loads user enviroment before calling the method.
        
        Returns:
            If successes: response object and a string with the  std_out of
            the execution. Raises an exception otherwise.
        
        Rises Exceptions:
            ExceptionRemoteNotSetup: Remote end point does not have sremote or
                the version of remote-local sites don't match.
            ExceptionRemoteModulesError: Remote end-point does not have
                module_name or required_registered_modules or versions don't
                match.
            
        """
        if (not isinstance(args, types.ListType) and 
            not isinstance(args, types.DictType)):
            raise Exception("Wrong type for args, expected list or dict, found "
                            + str(type(args)))
        # Encodes and sends the call request to the remote host and calls the
        # interpreter to execute. Then the response is retrieved in a 
        # serialized format..
        response_encoded, std_out = self._comms_client.place_and_execute(
            remote.encode_call_request(module_name, method_name,
                                    args, required_extra_modules =
                                        self._registered_remote_modules,
                                    remote_env_variables=
                                        self._remote_env_variables,
                                    conditional_remote_env_variables=
                                        self._conditional_remote_env_variables),
                                    keep_env=keep_env)
        
        success, response = remote.decode_call_response(response_encoded)
        if (success):
            return response, std_out
        else:
            if response!=None:
                if (type(response) is dict):
                    if response.has_key("sremote_type"):
                        raise remote.ExceptionRemoteExecError(response[
                                                                "message"])
            
            raise remote.ExceptionRemoteNotSetup(
                "Error executing " +module_name+"."+ method_name + "\n  Output:"
                +str(std_out))

        
    def do_bootstrap_install(self):
        """
        Uses _comms_client to configure the sremote environment in the remote
        machine including:
        - Creation of a ~/.sremote folder. Actual folder is defined by the 
          chosen ClientChannel. This folder will contain the scripts and
          python environment needed by sremote.
        - Deployment of the setup_bootstrap.sh, interpreter.sh, and
          remote_server.py script.
        - Remote call of the setup_bootstrap.sh script: Does environment 
          configuration.
        - Remote installation of the sremote library.
        
        Returns:
            True if success.
        """
        install_dir = self._comms_client.get_dir()
        self._comms_client.execute_command("/bin/mkdir", ["-p", install_dir])
        if not self._comms_client.push_file(
                                self.get_resource_route("setup_bootstrap.sh"), 
                                install_dir+"/setup_bootstrap.sh"):
            print "Error placing installation script."
            return False
        if not self._comms_client.push_file(
                                self.get_resource_route("interpreter.sh"), 
                                install_dir+"/interpreter.sh"):
            print "Error placing csh interpreter script"
            return False
        if not self._comms_client.push_file(
                               self.get_resource_route("remote_server.py"), 
                               install_dir+"/remote_server.py"):
            print "Error placing python interpreter script."
            return False
        output, err, rc = self._comms_client.execute_command("/bin/csh", 
                            [install_dir+"/setup_bootstrap.sh"])
        print "Install result:", rc, output, err
        self.do_install_git_module("https://github.com/gonzalorodrigo/qdo_interpreter.git",
                                   "integration")
        return True
    
    def do_install_git_module(self, git_url, branch=None, keep_after=None):
        """
        Installs a Python library in the remote host's sremote environment. The
        source of this library is a git repository. It takes two steps:
        - Deployment of the install_git_module.sh script.
        - Remote Invocation of the script that will download the library and
          install it in the environment.
        
        Args:
            git_url: a string with the http(s) url of the repository. This
                installer assumes that there is a py folder in the repo with a
                setup.py script.
            branch: a string with the name of the branch to install. If not set,
                master branch is installed.
            keep_after: if set with a string test, the git module code will be
                installed in ~/.sremote/tmp/[keep_after] and not deleted at 
                after installation clean up.
        
        Returns:
            true if installation successes. 
        """
        install_dir = self._comms_client.get_dir()
        if not self._comms_client.push_file(
                            self.get_resource_route("install_git_module.sh"), 
                            install_dir+"/install_git_module.sh"):
            print "Error placing installation script."
            return False
        branch_arg = []
        if branch:
            branch_arg.append(branch)
        if keep_after:
            branch_arg.append(keep_after)
        output, err, rc = self._comms_client.execute_command("/bin/csh", 
                        [install_dir + "/install_git_module.sh", git_url] +
                        branch_arg)
        print "Install result:", rc, output, err
        return True
    
    def get_resource_route(self, resource, package = "sremote.res"):
        # copied from pkg_util.get_data()
        
        loader = get_loader(package)
        if loader is None or not hasattr(loader, 'get_data'):
            return None
        mod = sys.modules.get(package) or loader.load_module(package)
        if mod is None or not hasattr(mod, '__file__'):
            return None
    
        # Modify the resource name to be compatible with the loader.get_data
        # signature - an os.path format "filename" starting with the dirname of
        # the package's __file__
        parts = resource.split('/')
        parts.insert(0, os.path.dirname(mod.__file__))
        resource_name = os.path.join(*parts)
        return resource_name
    
    def register_remote_module(self, module_name):
        """When a remote call is performed, Module module_name version 
        will be compared between local and remote. If not present in remote or
        version miss-match then ExceptionRemoteModulesError
        will be raised."""
        if not module_name in  self._registered_remote_modules:
            self._registered_remote_modules.append(module_name)
    
    def register_remote_env_variable(self, name, value, only_if_no_set=False):
        """When a remote call is perfomed, environment variable *name*
        will be set in the remote environment with value *value*. If conditional
        is True, this variable will be set ONLY if it is not set already."""
        if only_if_no_set:
            self._conditional_remote_env_variables[name] = value
        else:
            self._remote_env_variables[name]=value


class ClientChannel(object):
    """
    A ClientChannel is an abstract class interact with a remote host sremote
    environment (if installed). It provides implementation to: Place a method
    call request in a remote host and invoke the sremote interpreter to execute,
    and retrieve the result. This implementation realies on the presence of the
    sremote iterpreter script in the remote host.
    
    A class implementing ClientChanel shouldn implement method to:
    - Copy a file from the remote host to the local host (retrieve).
    - Copy a file from the local host to the remote host (push).
    - Execute a command in the remote host.
    - Detect the home directory of the user used to access the remote user.

    """
    
    def execute_request(self, method_request_reference, 
                        method_response_reference, keep_env=False):
        """Invokes the remote interpreter to execute a method request.
        
        Args:
            method_request_reference: string with the absolute file route
                pointing  to a file present in the remote file system. This file
                contains the serialized version of a method call request.
            mothod_response_reference: string with absolute file route pointing
                to a file in a existing remote host directory. The result of
                executing the call request will be stored in that file in a
                serialized format.
            keep_env: loads the user enviroment nefore executing the request.
        
        Returns:
            a string containing the standard output generated by the
            invocation of the interpreter.
            
        """
        
        output= self.execute_command("/bin/csh", 
                               [self.get_dir()+"/"+self._interpreter_route, 
                               method_request_reference, 
                               method_response_reference], keep_env=keep_env)
        
        return output

    
    # Implemented methods
    def place_and_execute(self, serialized_method_call_request, keep_env=False):
        """Places method call request in the remote host, executes it, 
        retrives the serialized content of the response.

        Args:
            serialized_method_call_request: serialized versions of the method
                call request.

        Returns:
            a string containing the serialized version of the method response
            genereated by the execition of serielized_method_call_request. Also
            returns a string with  standard output of the execution of the
            remote interpreter.
        """
        response_location = self.gen_remote_response_reference()
        location = self.place_call_request(serialized_method_call_request)
        output = self.execute_request(location, response_location,
                                      keep_env=keep_env)
        return self.retrieve_call_response(response_location), output

    def place_call_request(self, serialized_method_call_request):
        """Places a serialized method call request in the remote host.
        
        Args:
            serialized_method_call_request: string containing the serialized
                version of the request.
        
        Returns: 
            a string with a valid remote file system route to the file
            where the request has been placed.
        """
       
        reference_route = self.get_local_temp_file_route()
        text_file = open(reference_route, "w")
        text_file.write(serialized_method_call_request)
        text_file.close()
        remote_file_route = self.gen_remote_temp_file_route()
        self.push_file(reference_route, remote_file_route)
        return remote_file_route
    
    def retrieve_call_response(self, method_responde_reference):
        """Retrieves a file from the remote host containing a method call
        response, and returns its content.
        
        Args: 
            method_responde_reference: string with a value remote file system
            file route. It points to a file containing a method call response.
        
        Returns:
            string with the content of the remote pointed file.  
        """
        local_route_response = self.get_local_temp_file_route(False)
        if not self.retrieve_file(method_responde_reference,
                                  local_route_response):
            raise remote.ExceptionRemoteNotSetup("retrieve_call_response: " +
                                                  "Result of method could not" +
                                                  " be retrieved. Pointer: " +
                                                  str(method_responde_reference)
                                                  )
        text_file = open(local_route_response, "r")
        content = "\n".join(text_file.readlines())
        text_file.close()
        return content
    def gen_remote_response_reference(self):
        """Returns a string with a valid remote filesystem route where a
        response will be stored."""
        return self.gen_remote_temp_file_route(False)
    
    def gen_remote_temp_file_route(self, in_file=True):
        """Returns a string with a remote  flesystem route where a
        temporary can be stored.
        Args:
            in_file: if true the file name will be appended .out
        """
        file_name = self.get_dir()+"/tmp/"+self.gen_random_file_name()
        if not in_file:
            file_name+=".out"
        return file_name
    def get_local_temp_file_route(self, in_file=True):
        """Returns a string with a local filseystem route where a file
        can be stored.
        
        Args:
            in_file: if true the file name will be appended .out"""
        file_name = "/tmp/"+self.gen_random_file_name()
        if not in_file:
            file_name+=".out"
        return file_name
    
    def gen_random_file_name(self):
        """returns a true random file name starting with the current time
        followed by a uuid1:
        [year]-[month]-[day]_[hour]-[minute]-[second].[us]-[uuid1].dat"""
        
        random_name = str(datetime.datetime.now())
        random_name = random_name.replace(" ", "_").replace(":","-")
        random_name += "-"+ str(uuid.uuid1())+".dat"
        return random_name
 
    def get_dir(self):
        """Returns a string with the remote file system location of the sremote
        environment."""
        return self.get_home_dir()+"/.sremote"
    
    def get_pwd(self):
        """Connects to the remote server and detects the user default after
        login directory."""
        dir_string =  self.execute_command("/bin/pwd")[0]
        return dir_string.replace("\n", "").replace("\r","")
 
    # OS and comms channel dependant methods to be implemented by the concrete
    # implementations of the classs.
    def push_file(self, origin_route, dest_route):
        """Copies a file from the local to the remote host
        Args:
            origin_route: string with a valid local filesystem file route
                pointing to the file to be copied.
            dest_reoute: string with a valid remote filesystem file route
                pointing to the where the file should be copied.
        Returns: 
            True if successful.
        """
        raise Exception("Non implemented")
    
    def retrieve_file(self, origing_route, dest_route):
        """Copies a file from the remote to the local host
        Args:
            origin_route: string with a valid remote filesystem file route
                pointing to the file to be copied.
            dest_reoute: string with a valid local filesystem file route
                pointing to the where the file should be copied.
        Returns: 
            True if successful.
        """
        raise Exception("Non implemented")
    
    def execute_command(self, command, arg_list=[], keep_env=False):
        """Executes a command in the remote host as a user. It is executed
        in the context of the default after login directory of the user.
        
        Args:
            Command: executable to be invoked.
            arg_list: List of the arguments to be passed to the command.
            keep_eng: loads user enviroment before executing command.
        Returns:
            std_out (string), error_out (string) and status code produced
        """
        raise Exception("Non implemented")
    
    def get_home_dir(self):
        """Retrieves the home directory of the user that is used to connect
        to the remote host."""
        raise Exception("Non implemented")
    

    
    
class ServerChannel(object):    
    """This class implements the server side of the sremote library.  There is
    no need of specific implementation like on the client side. This code
    receives request and return response through files."""
    def process_call_request(self, method_call_request_pointer,
                             method_response_pointer):
        """Executes a method of and returns its result encoded and
        serialized as a call response. This method is called by the interpreter. 
        Args:
            method_call_request_pointer: string with a reference to file
            containing a method call request. It is retrieved, deserialized and
            decoded. 
            method_response_pointer: string with a local (to the remote host)
            filesystem location where the serialized version of the method call
            response should be stored.

        Returns:
            string with the serialized encoded call result object, containing
            what the executed method returned.
        """
        call_request_serialized = self.retrieve_call_request(
            method_call_request_pointer)
        target_obj_name, command_name, args, extra_modules, env_variables  = \
                remote.decode_call_request(call_request_serialized)
        remote.set_environ_variables(env_variables)
        #print call_request_serialized, target_obj_name
        success = True
        try:
            reponse_obj = remote.call_method_object(target_obj_name,
                                                    command_name, args)
        except remote.ExceptionRemoteExecError as e:
            success = False
            reponse_obj = e.get_serialized()
        content = remote.encode_call_response(reponse_obj, success,
                                              required_extra_modules=
                                               extra_modules)
        self.store_call_response(method_response_pointer, content)
        return content
        

    def retrieve_call_request(self, method_request_reference):
        """Returns the contend of a file pointed by the
        method_request_reference."""
        text_file = open(method_request_reference, "r")
        content = "\n".join(text_file.readlines())
        text_file.close()
        return content
    def store_call_response(self, reference_route, content):
        """Stores the string content in a reference_route in the local
        location reference_route."""
        text_file = open(reference_route, "w")
        text_file.write(content)
        text_file.close()
    def return_error(self):
        """Returns a tring with the serialised version of failed method
        response.""" 
        return remote.encode_call_response({}, False)
