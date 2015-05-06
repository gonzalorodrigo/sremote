import remote_api
import subprocess


class QDORemoteClient(remote_api.RemoteClient):
    def qsummary(self):
        return_value = self.do_remote_call("qsummary")
        print return_value


_interpreter_route="./qdo_interpreter_sim.sh"

class QDOLocalConnector(remote_api.CommsChannel):
    """
    Base class for the client side of the remoting functions


    """
    def __init__(self, hostname="hopper"):
        self._hostnamm = hostname


    def execute_request(self, method_request_reference):
        p = subprocess.Popen([_interpreter_route, method_request_reference], stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc

    def place_call_request(self, serialized_method_call_request, reference_route=None):
        if reference_route == None:
            reference_route = self.gen_random_file_route()
        text_file = open(reference_route, "w")
        text_file.write(serialized_method_call_request)
        text_file.close()
        return reference_route

    def gen_random_file_route(self):
        return "file_name.dat"
        
    def retrieve_call_request(self, method_request_reference):
        text_file = open(method_request_reference, "r")
        content = "\n".join(text_file.readlines())
        return content
 