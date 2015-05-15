""" 
Classes to do remote Python functions calls.

This code allows to call remote functions of methods that receive and return
serializable objects. 

If code is going to be remoted, the key work is to create a subclass of
CommsChannel. That class has to have specific methods to invoke the remote
endpoint, indicate the desired method to be executed, pass the input arguments,
retrieve the result, and interpret it. 

To send a remote call, a client needs to create a RemoteClient with the
adequate comms_client. Then do_remote_call is invoked with the name of the
methods and a list of the arguments.

qdo_remote_api_sim is an example: the communication channel are files on the
file system. It implements 
    - place_call_request: encodes and serializes the method name and
      arguments. Puts them in a file in the file system.
    - process_call_request: invoked by the end point when a request is received.
      it deserializes the request and invokes que code.
    - end point: is a shell file that is invoked by using subprocess. It
      receives the method call request file location as an argument. Then,
      it calls a the process_call_request, with the QDO object.
    - retrive_call_request: it reads the std_out of the end point execution,
      deserializes and extracts the result.

In the example qdo_remote_api_sim: 
    - qdo_interpreter.sh is the end point.
    - qdo_remote_api_sim.py defines the comms_client to use the end point.
    - qdo_remote_server.py is called by the end point to call the remote method.
    - test_qdo_remote.py is a sample usage of how everything is invoked.
    - method call requests are stored as files. The references to them are just
      file system routes. 
"""

import sremote.tools as remote


class RemoteClient(object):

    """
    Base class for the client side of the remoting functions

    During creation it receives a comms_client that will communicate with the
    end point. 
    """

    def __init__(self, comms_client):
        """Init of the class

        Args:
            comms_client: an object that is super class of RemoteComms class.
        """
        self._comms_client = comms_client

    def do_remote_call(self, module_name, method_name, args=[]):
        """ Uses _comms.client to send a request to execute method_name with
        args.

        Args:
            method_name: name of the method to be executed.
            args: list with the arguments.
        """
        std_out, std_err, status = self._comms_client.place_and_execute(
            remote.encode_call_request(module_name, method_name,
                                       args))
        success, response = remote.decode_call_response(std_out)
        if (success):
            return response
        else:
            raise Exception(
                "Error executing " +module_name+"."+ method_name + "\n  Output:"
                 + str(std_out) + "\n  Error:" + str(std_err))

        
    def do_bootstrap_install(self):
        install_dir = self._comms_client.get_dir()
        print "INSTALLDIR", install_dir
        self._comms_client.execute_command("mkdir", ["-p", install_dir])
        if not self._comms_client.push_file("./setup_bootstrap.sh", 
                                   install_dir+"/setup_bootstrap.sh"):
            print "Error placing installation script."
            return False
        if not self._comms_client.push_file("./interpreter.sh", 
                               install_dir+"/interpreter.sh"):
            print "Error placing interpreter script"
            return False
        if not self._comms_client.push_file("./remote_server.py", 
                               install_dir+"/remote_server.py"):
            print "Error placing interpreter script"
            return False
        output, err, rc = self._comms_client.execute_command("/bin/csh", 
                            [install_dir+"/setup_bootstrap.sh"])
        print "Install result:", rc, output, err
        self.do_install_git_module("https://github.com/gonzalorodrigo/qdo_interpreter.git",
                                   "modular")
        return True
    
    def do_install_git_module(self, git_url, branch=None):
        install_dir = self._comms_client.get_dir()
        if not self._comms_client.push_file("./install_git_module.sh", 
                                   install_dir+"/install_git_module.sh"):
            print "Error placing installation script."
            return False
        branch_arg = []
        if branch:
            branch_arg.append(branch)
        output, err, rc = self._comms_client.execute_command("/bin/csh", 
                        [install_dir + "/install_git_module.sh", git_url] +
                        branch_arg)
        print "Install result:", rc, output, err
        return True
        


class ClientChannel(object):

    """Base class for the communication in this remoting schema. 

    This class has the responsibility of providing an interface with/from the
    end point. 
    """


    def place_and_execute(self, serialized_method_call_request):
        """Sends the method call request as an item that can be referenced. 
        Invokes the endpoint with that reference so it processes the
        call. 

        Args:
            serialized_method_call_request: serialized versions of the method
            call request.

        Returns: 
            reference to the serialeized method request.
        """
        response_location = self.gen_remote_response_reference()
        location = self.place_call_request(serialized_method_call_request)
        output = self.execute_request(location, response_location)
        return self.retrieve_call_response(response_location), output

    def gen_remote_response_reference(self):
        raise Exception("Non implemented")
    
    def retrieve_call_response(self, method_responde_reference):
        raise Exception("Non implemented")
    
    def place_call_request(self, serialized_method_call_request,
                           reference_route=None):
        """Sends a method call request to the end point. 

        Args:
            serialized_method_call_request: serialized version of the request.
            reference_route: if set, the reference that the endpoint should use
            to find the request. If not, that reference will be calculated by
            this method.

        Returns:
            reference used to store the request.

        """
        raise Exception("Non implemented")
    def execute_request(self, method_request_reference):
        """Invokes the endpoint so it uses the referenced method call request,
        processes it, and executes the corresponding method.

        Args:
            method_request_reference: reference for the endpoint to find the
            methods call request.

        Returns:
            whatever the method called returns.
        """

        raise Exception("Non implemented")
    
    def copy_file(self, origin_route, dest_route):
        raise Exception("Non implemented")
    
    def retrieve_file(self, origing_route, dest_route):
        raise Exception("Non implemented")
    
    def execute_command(self, command, arg_list=[]):
        raise Exception("Non implemented")
    
    def get_home_dir(self):
        raise Exception("Non implemented")
    def get_dir(self):
        return self.get_home_dir()+".sremote/generic"
    
    
class ServerChannel(object):    
    
    def process_call_request(self, method_call_request_pointer,
                             method_response_pointer):
        """Executes a method of target_obj and returns its result encoded and
        serialized as a call response. This method is executed in the end point. 


        Args:
            targe_obj: object whose method will be executed.
            method_call_request_pointer: reference to find the method call
            request. It is retrieved, deserialized and decoded. 

        Returns:
            serialized encoded call result object, containing what the executed
            method of target_obj returned.
        """
        call_request_serialized = self.retrieve_call_request(
            method_call_request_pointer)
        target_obj_name, command_name, args = remote.decode_call_request(
            call_request_serialized)
        print call_request_serialized, target_obj_name
        reponse_obj = remote.call_method_object(target_obj_name, command_name, args)
        content = remote.encode_call_response(reponse_obj, True)
        self.store_call_response(content, method_response_pointer)
        return content
        

    def retrieve_call_request(self, method_request_reference):
        """Retrieves a method_request_reference without transfomring it.
         This method is executed in the end point  
        """
        raise Exception("Non implemented")

    def return_error(self):
        return remote.encode_call_response({}, False)
