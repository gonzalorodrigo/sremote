import sremote.api as remote_api
import subprocess


class LocalConnector(remote_api.CommsChannel):

    """
    Connector for remoting functions. It relaies on executing a shell script
    in the same directory as the code. The route to such script can be
    configured in creation time.
    """
    def __init__(self, interpreter_route = "./interpreter.sh"):
        self._interpreter_route = interpreter_route

    def execute_request(self, method_request_reference):
        p = subprocess.Popen(
            [self._interpreter_route, method_request_reference], 
                stdout=subprocess.PIPE)
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

