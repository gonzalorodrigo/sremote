import remote_api
import subprocess


class QDORemoteClient(remote_api.RemoteClient):
    def qsummary(self):
        return_value = self.do_remote_call("qsummary")
        print return_value


<<<<<<< HEAD
_interpreter_route="./qdo_interpreter_sim.sh"
=======
_interpreter_route="./qdo_interpreter.sh"
>>>>>>> 488dcb672ca76f8ec5c208e6941d3713eb526496

class QDOLocalConnector(remote_api.CommsChannel):
    """
    Base class for the client side of the remoting functions


    """
    def __init__(self, hostname="hopper"):
        self._hostnamm = hostname


<<<<<<< HEAD
    def execute_request(self, method_request_reference):
        p = subprocess.Popen([_interpreter_route, method_request_reference], stdout=subprocess.PIPE)
=======
    def execute_request(self, arg):
        p = subprocess.Popen([_interpreter_route, arg], stdout=subprocess.PIPE)
>>>>>>> 488dcb672ca76f8ec5c208e6941d3713eb526496
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc

<<<<<<< HEAD
    def place_call_request(self, serialized_method_call_request, reference_route=None):
        if reference_route == None:
            reference_route = self.gen_random_file_route()
        text_file = open(reference_route, "w")
        text_file.write(serialized_method_call_request)
        text_file.close()
        return reference_route
=======
    def place_call_request(self, content, file_route=None):
        if file_route == None:
            file_route = self.gen_random_file_route()
        text_file = open(file_route, "w")
        text_file.write(content)
        text_file.close()
        return file_route
>>>>>>> 488dcb672ca76f8ec5c208e6941d3713eb526496

    def gen_random_file_route(self):
        return "file_name.dat"
        
<<<<<<< HEAD
    def retrieve_call_request(self, method_request_reference):
        text_file = open(method_request_reference, "r")
=======
    def retrieve_call_request(self, content_pointer):
        text_file = open(content_pointer, "r")
>>>>>>> 488dcb672ca76f8ec5c208e6941d3713eb526496
        content = "\n".join(text_file.readlines())
        return content
 