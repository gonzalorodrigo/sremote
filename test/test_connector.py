import calendar
import os
import time
import unittest

class TestClientChannel(unittest.TestCase):
    """Abstract class to define unnittests for specific implementations of
     sremote.ClientChannel.
    """
    
    def test_homedir(self):
        raise NotImplementedError
        
    #- Checks the basic function to login-in 
    def test_status(self):
        raise NotImplementedError
        
    def test_push_get_file(self):
        orig_route= _get_current_dir()+"/file.tmp"
        _create_file(orig_route, "Hola!")
        
        dest_route = "/tmp/file.{0}.tmp".format((calendar.timegm(time.gmtime()))
                                                )
        local_dest_route=_get_current_dir()+"/download.tmp"
        
        self.assertFalse(self._connector.retrieve_file(dest_route, 
                                                       local_dest_route))
        
        self.assertTrue(self._connector.push_file(orig_route, dest_route))
        
        
        if (os.path.isfile(local_dest_route)):
            os.remove(local_dest_route)
        self.assertTrue(self._connector.retrieve_file(dest_route, 
                                                      local_dest_route))
        
        local_file = file(local_dest_route, "r")
        self.assertEqual("Hola!", local_file.read())
        local_file.close()
        
    def test_delete_file(self):
        orig_route=_get_current_dir()+"/del_file.tmp"
        _create_file(orig_route, "I should be deleted!")
        dest_route = "/tmp/file.{0}.tmp".format((calendar.timegm(time.gmtime()))
                                                )
        self.assertTrue(self._connector.push_file(orig_route, dest_route))
        
        self.assertTrue(self._connector.delete_file(dest_route))
        
        local_dest_route=_get_current_dir()+"/download.tmp"
        
        self.assertFalse(self._connector.retrieve_file(dest_route, 
                                                       local_dest_route))
    
    def test_execute_command(self):
        output, error, rc= self._connector.execute_command("/bin/echo", 
                                                           ["hola"])
        self.assertEqual(rc, 0)
        self.assertEqual(output, "hola")
        self.assertEqual(error, "")
        
        output, error, rc= self._connector.execute_command("/bin/echoN", 
                                                           ["hola"])
        self.assertEqual(rc, -1)
    
    def test_do_self_discovery(self):
        
        pass
        
    def test_get_dir_sremote(self):
        
        pass
    
    def test_place_and_execute(self):
        pass
    
def _get_current_dir():
    return os.path.dirname(os.path.realpath(__file__));

def _create_file(route, content):
    orig_file = file(route, "w")
    orig_file.write(content)
    orig_file.close()
        
        
    
