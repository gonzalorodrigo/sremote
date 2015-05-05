


import remote_api as remote


class RemoteClient:
    """
    Base class for the client side of the remoting functions

    Code to be remoted, will superclass this class and add the methods of the
    API calling the do_remote_call with the corresponding arguments.
    
    During creation it receives a CommsClient that will communicate with the
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
