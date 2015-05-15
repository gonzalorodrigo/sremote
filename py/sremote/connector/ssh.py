import sremote.api as remote_api
import subprocess


class ClientSSHConnector(remote_api.ClientChannel):

    def __init__(self, hostname):
        self._hostname = hostname;
    

    def auth(self, username):
        self._username = username
        self._home_dir = self.get_pwd()
 
    def push_file(self, origin_route, dest_route):
        command_list =  ["scp", origin_route, self._username + "@" +
                         self._hostname + ":" + dest_route]
        print command_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if (rc!=0):
            print "File push operation error", output, err
        return rc == 0
    
    def retrieve_file(self, origin_route, dest_route):
        command_list =  ["scp", self._username + "@" +
                 self._hostname + ":" + origin_route,  dest_route]
        print command_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if (rc!=0):
            print "File retrieve operation error", output, err
        return rc == 0
        
    def execute_command(self, command, arg_list=[]):
        command_list = ["ssh", self._username+"@"+self._hostname, 
                        command] + arg_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc
    
    def get_home_dir(self):
        return self._home_dir
    

