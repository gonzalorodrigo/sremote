import remote_api
import subprocess


class QDORemoteClient(remote_api.RemoteClient):
    def qsummary(self):
        return_value = self.do_remote_call("qsummary")
        print return_value


_interpreter_route="./qdo_interpreter.sh"

class QDOLocalConnector(remote_api.CommsChannel):
    """
    Base class for the client side of the remoting functions


    """
    def __init__(self, hostname="hopper"):
        self._hostnamm = hostname


    def execute_request(self, arg):
        p = subprocess.Popen([_interpreter_route, arg], stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc

    def place_call_request(self, content, file_route=None):
        if file_route == None:
            file_route = self.gen_random_file_route()
        text_file = open(file_route, "w")
        text_file.write(content)
        text_file.close()
        return file_route

    def gen_random_file_route(self):
        return "file_name.dat"
        
    def retrieve_call_request(self, content_pointer):
        text_file = open(content_pointer, "r")
        content = "\n".join(text_file.readlines())
        return content
 