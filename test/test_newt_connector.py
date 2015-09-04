"""UNIT TESTS for newt connector. It requires to use a valid
NERSC account that can be used to establish a NEWT session. Environemnt
variables required:
- QDO_NEWT_USER = valid NERSC user.
- QDO_NEWT_PASSWORD = corresponding password.
- QDO_NEWT_SITE = name of a NERSC site to do the tests against (e.g.
  edison, hopper, cori). If not set it will use edion 


 python -m unittest test_newt_connector.TestNewt
 
"""

from test_connector import TestClientChannel
import os
import sremote.connector.newt as newt

class TestNewt(TestClientChannel):
    
    def setUp(self):
        self._username = os.getenv("QDO_NEWT_USER", None)
        self._password = os.getenv("QDO_NEWT_PASSWORD", None)
        self._site = os.getenv("QOD_NEWT_SITE", "edison")
        if self._username is None:
            raise ValueError, "Missing QDO_NEWT_USER env var"
        if self._password is None:
            raise ValueError, "Missing QDO_NEWT_PASSWORD env var"
        
    
        self._connector  = newt.ClientNEWTConnector(self._site)
        self.assertTrue(self._connector.auth(username=self._username,
                                             password=self._password))
    

    def test_homedir(self):
        self.assertIn(self._username, self._connector.get_home_dir())
        
        new_connector = newt.ClientNEWTConnector(self._site)

        self.assertTrue(new_connector.auth(username=self._username,
                                        password=self._password,
                                        home_dir="/tmp"))
        self.assertEqual(new_connector.get_home_dir(), "/tmp")
        
    
    def test_token_auth(self):
        token = self._connector._token
        
        conn1 = newt.ClientNEWTConnector(self._site)
        self.assertTrue(conn1.auth(username=self._username,
                                           token=token))
        
        self.assertTrue(conn1.status())
        
        conn2 = newt.ClientNEWTConnector(self._site)
        self.assertFalse(conn2.auth(username="user",
                                            password="pass"))

        conn3 = newt.ClientNEWTConnector(self._site)
        self.assertFalse(conn3.auth(username=self._username,
                                            token="Loren Ipsum"))
    #- Checks the basic function to login-in 
    def test_status(self):
        self.assertTrue(self._connector.status())
        
        #- we brake internal cookie so status fails.
        self._connector._token = "Loren Ipsum"
        self.assertFalse(self._connector.status())
        
    
    