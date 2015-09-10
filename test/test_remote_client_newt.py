"""UNIT TESTS for sermote client that uses a NEWT connector. Environemnt
variables required:
- QDO_NEWT_USER = valid NERSC user.
- QDO_NEWT_PASSWORD = corresponding password.
- QDO_NEWT_SITE = name of a NERSC site to do the tests against (e.g.
  edison, hopper, cori). If not set it will use edion 


 python -m unittest test_remote_client_newt.TestRemoteClientNEWT
 
"""


from test_remote_client import TestRemoteClient 
import sremote.connector.newt as newt
from getpass import getuser
import os

class TestRemoteClientNEWT(TestRemoteClient):
    
    
    def create_connector(self):
        self._username = os.getenv("QDO_NEWT_USER", None)
        self._password = os.getenv("QDO_NEWT_PASSWORD", None)
        self._site = os.getenv("QOD_NEWT_SITE", "edison")
        if self._username is None:
            raise ValueError, "Missing QDO_NEWT_USER env var"
        if self._password is None:
            raise ValueError, "Missing QDO_NEWT_PASSWORD env var"
        new_connector  = newt.ClientNEWTConnector(self._site)
        self.assertTrue(new_connector.auth(username=self._username,
                                             password=self._password))
        return new_connector
            