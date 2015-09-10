"""UNIT TESTS for sermote client that uses an ssh connector. It executes
locally and requires that the current user can do "passwordless" ssh to
localhost.


python -m unittest test_remote_client_ssh.TestRemoteClientSSH
 
"""


from test_remote_client import TestRemoteClient 
from sremote.connector.ssh import ClientSSHConnector 
from getpass import getuser

class TestRemoteClientSSH(TestRemoteClient):
    
    
    def create_connector(self):
        self._username = getuser()
        self._site="localhost"
        new_connector = ClientSSHConnector(self._site)
        self.assertTrue(new_connector.auth(username=self._username))
        return new_connector
            