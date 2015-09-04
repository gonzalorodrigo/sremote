"""UNIT TESTS for ssh connector. It executes locally and requires that
the current user can do "passwordless" ssh to localhost.


 python -m unittest test_ssh_connector
 
"""

from test_connector import TestClientChannel
import sremote.connector.ssh as ssh
from getpass import getuser

class TestSsh(TestClientChannel):
    
    def setUp(self):
        self._username = getuser()
        self._site = "localhost"
        self._connector = ssh.ClientSSHConnector(self._site)
        self.assertTrue(self._connector.auth(username=self._username))
    

    def test_homedir(self):
        self.assertIn(self._username, self._connector.get_home_dir())
        
        new_connector = ssh.ClientSSHConnector(self._site)

        self.assertTrue(new_connector.auth(username=self._username,
                                        home_dir="/tmp"))
        self.assertEqual(new_connector.get_home_dir(), "/tmp")
        
    
    def test_no_auth(self):
        pass
    
    #- Checks the basic function to login-in 
    def test_status(self):
        self.assertTrue(self._connector.status())
    
    