


import remote_tools as remote


class RemoteClient(object):
    """
    Base class for the client side of the remoting functions

    Code to be remoted, will superclass this class and add the methods of the
    API calling the do_remote_call with the corresponding arguments.
    
    During creation it receives a comms_client that will communicate with the
    server.
    """

    def __init__(self, comms_client):
        """Initiazliation of the class
        
        Args:
            comms_client: an object that is super class of RemoteComms class.
        """
        self._comms_client = comms_client

    def do_remote_call(self, method_name, args=[]):
        """ Uses _comms.client to send a request to execute method_name with
        args.
        
        Args:
            method_name: name of the method to be executed.
            args: list with the arguments.
        """
        std_out, std_err, status = self._comms_client.place_and_execute(
            remote.encode_call_request(method_name,
                                       args))

        success, response = remote.decode_call_response(std_out)
        if (success):
            return response
        else:
            raise Exception(str(response))


class CommsChannel(object):
    """
    


    """

    def place_and_execute(self, content):
        location = self.place_call_request(content)
        return self.execute_request(location)

    def execute_request(self, arg):
        raise Exception("Non implemented")

    def place_call_request(self, content, file_route=None):
        raise Exception("Non implemented")
    
    def process_call_request(self, target_obj, method_call_request_pointer):
        call_request_serialized = self.retrieve_call_request(
                                  method_call_request_pointer)
        command_name, args = remote.decode_call_request(call_request_serialized)
        reponse_obj = remote.call_method_object(target_obj, command_name, args)
        return remote.encode_call_response(reponse_obj, True)
    
    def retrieve_call_request(self, content_pointer):
        raise Exception("Non implemented")
    
    def return_error(self):
        return remote.encode_call_response({}, False)
    
    

