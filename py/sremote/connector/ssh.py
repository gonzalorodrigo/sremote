import sremote.api as remote_api
import subprocess


class ClientSSHConnector(remote_api.ClientChannel):

    """
    Connector for remoting functions. It relaies on executing a shell script
    in the same directory as the code. The route to such script can be
    configured in creation time.
    """
    def __init__(self, hostname, interpreter_route = "./interpreter.sh"):
        self._interpreter_route = interpreter_route
        self._hostname = hostname;
    
    
    
    def auth(self, username):
        self._username = username
        self.home_dir = self.execute_command("pwd")
        

    def execute_request(self, method_request_reference):
        return self.execute_command(self._interpreter_route, 
                               method_request_reference)

    def place_call_request(self, serialized_method_call_request, reference_route=None):
        if reference_route == None:
            reference_route = self.gen_random_file_route()
        text_file = open(reference_route, "w")
        text_file.write(serialized_method_call_request)
        text_file.close()
        return reference_route

    def gen_random_file_route(self):
        return "file_name.dat"
    
    def copy_file(self, origin_route, dest_route):
        command_list =  ["scp", origin_route, self._username + "@" +
                         self._hostname + ":" + dest_route]
        print command_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if (rc!=0):
            print "File copy operation error", output, err
        return rc == 0
        
    def execute_command(self, command, arg_list=[]):
        command_list = ["ssh", self._username+"@"+self._hostname, 
                        command] + arg_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc
         


class ServerSSHConnector(remote_api.ServerChannel):
    def retrieve_call_request(self, method_request_reference):
        text_file = open(method_request_reference, "r")
        content = "\n".join(text_file.readlines())
        return content



