"""Implementation of the sremote.api.ClientChannel class that uses SSH as
the communication channel. It uses scp and direct ssh execution."""


import sremote.api as remote_api
import subprocess


class ClientSSHConnector(remote_api.ClientChannel):

    def __init__(self, hostname, interpreter_route = "interpreter.sh"):
        self._interpreter_route = interpreter_route
        self._hostname = hostname;

    def auth(self, username, password=None, token=None, home_dir=None):
        """Auth method. It stores the username. Authenticaion does not
        occur until an actual operation is executed. It no ssh key is
        configured in the client, future operations will ask for password."""
        self._username = username
        self._home_dir = self.get_pwd()
        self._token = username
        return self.status()
    
    def status(self):
        """Returns true if the username could login"""
        return self._home_dir!=""
 
    def push_file(self, origin_route, dest_route):
        command_list =  ["scp", origin_route, self._username + "@" +
                         self._hostname + ":" + dest_route]
        #print command_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if (rc!=0):
            print "File push operation error", output, err
        return rc == 0
    
    def retrieve_file(self, origin_route, dest_route):
        command_list =  ["scp", self._username + "@" +
                 self._hostname + ":" + origin_route,  dest_route]
        #print command_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if (rc!=0):
            print "File retrieve operation error", output, err
        return rc == 0
    
    def delete_file(self, route):
        output, err, rc=self.execute_command("/bin/rm", [route])
        if rc!=0:
            print "File delete operation error", output, err
        return rc==0
        
        
    def execute_command(self, command, arg_list=[], keep_env=False):
        command_list = ["ssh", self._username+"@"+self._hostname, 
                        command] + arg_list
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc
    
    def get_home_dir(self):
        return self._home_dir
    

