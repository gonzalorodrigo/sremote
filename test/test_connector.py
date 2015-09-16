import calendar
import os
import sremote.tools as remote
import time
import unittest

from sremote.api import RemoteClient

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
        orig_route= get_current_dir()+"/file.tmp"
        create_file(orig_route, "Hola!")
        
        dest_route = "/tmp/file.{0}.tmp".format((calendar.timegm(time.gmtime()))
                                                )
        local_dest_route=get_current_dir()+"/download.tmp"
        
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
        orig_route=get_current_dir()+"/del_file.tmp"
        create_file(orig_route, "I should be deleted!")
        dest_route = "/tmp/file.{0}.tmp".format((calendar.timegm(time.gmtime()))
                                                )
        self.assertTrue(self._connector.push_file(orig_route, dest_route))
        
        self.assertTrue(self._connector.delete_file(dest_route))
        
        local_dest_route=get_current_dir()+"/download.tmp"
        
        self.assertFalse(self._connector.retrieve_file(dest_route, 
                                                       local_dest_route))
    
    def test_execute_command(self):
        output, error, rc= self._connector.execute_command("/bin/echo", 
                                                           ["hola"])
        output=output.split("\n")[0]
        self.assertEqual(rc, 0)
        self.assertEqual(output, "hola")
        self.assertEqual(error, "")
        
        output, error, rc= self._connector.execute_command("/bin/echoN", 
                                                           ["hola"])
    
    def test_set_get_sremote_dir(self):
        self._connector.set_sremote_dir("/tmp")
        self.assertEqual("/tmp", self._connector.get_dir_sremote())
    
    def test_get_pwd(self):
        self.assertEqual(self._connector.get_home_dir(), 
                         self._connector.get_pwd())
                
    def test_do_self_discovery_relative(self):
        self._connector.set_sremote_dir("/tmp/sremote_test/")
        self.assertTrue(self._connector.execute_command("/bin/mkdir",
                                            ["-p", 
                                             "/tmp/sremote_test/.sremote"]))
        local_disc_file  = get_current_dir()+"/selfdisc.rc"
        remote_disc_file = "/tmp/sremote_test/.sremote/selfdisc.rc"
        create_file(local_disc_file, """
            {"sremote": "/tmp/sremote_test/selfd",
            "relative_tmp": "local_tmp"
            }
        """)
        self._connector.push_file(local_disc_file, remote_disc_file)
        self._connector._home_dir="/tmp/sremote_test"
        self.assertTrue(self._connector.do_self_discovery(
                                                file_name="selfdisc.rc"))
        self.assertEqual(self._connector.get_dir_sremote(), 
                         "/tmp/sremote_test/selfd")
        self.assertEqual(self._connector.get_dir_tmp(), 
                         self._connector.get_home_dir()+"/local_tmp")
        
    def test_do_self_discovery_absolute(self):
        self._connector.set_sremote_dir("/tmp/sremote_test/")
        self.assertTrue(self._connector.execute_command("/bin/mkdir",
                                            ["-p", 
                                             "/tmp/sremote_test/.sremote"]))
        
        local_disc_file  = get_current_dir()+"/selfdisc.rc"
        remote_disc_file = "/tmp/sremote_test/.sremote/selfdisc.rc"
        create_file(local_disc_file, """
            {"sremote": "/tmp/sremote_test/selfd",
            "absolute_tmp": "/tmp/sremote_test/tmp"
            }
        """)
        self._connector._home_dir="/tmp/sremote_test"
        self._connector.push_file(local_disc_file, remote_disc_file)
        self.assertTrue(self._connector.do_self_discovery(
                                                file_name="selfdisc.rc"))
        self.assertEqual(self._connector.get_dir_sremote(), 
                         "/tmp/sremote_test/selfd")
        self.assertEqual(self._connector.get_dir_tmp(), 
                         "/tmp/sremote_test/tmp")
             
    def test_place_and_execute(self):
        self._configure_remote_environment()
        
        serialized_method_call_request = \
                remote.encode_call_request("os", "listdir",
                                        args=["/tmp/sremote_test/"])
        response, output, location, response_location = \
            self._connector.place_and_execute(serialized_method_call_request)
        code, function_return = remote.decode_call_response(response)
        self.assertIn("interpreter.sh", function_return)
        
    def test_remote_environemt(self):
        self._configure_remote_environment()
        
        serialized_method_call_request = \
                remote.encode_call_request("os", "getenv",
                                        args=["MYVAR",
                                             None],
                                        remote_env_variables =
                                            {"MYVAR":"MYVALUE"}
                                        )
        response, output, location, response_location = \
            self._connector.place_and_execute(serialized_method_call_request)
        code, function_return = remote.decode_call_response(response)
        self.assertEqual(function_return, "MYVALUE")
        
        serialized_method_call_request = \
                remote.encode_call_request("os", "getenv",
                                        args=["PATH",
                                             None],
                                        conditional_remote_env_variables =
                                            {"PATH":"MYVALUE"}
                                        )
        response, output, location, response_location = \
            self._connector.place_and_execute(serialized_method_call_request)
        code, function_return = remote.decode_call_response(response)
        self.assertNotEqual(function_return, "MYVALUE")
        
        serialized_method_call_request = \
        remote.encode_call_request("os", "getenv",
                                args=["PATH",
                                     None],
                                remote_path_addons =
                                    ["/impossible_dir"]
                                )
        response, output, location, response_location = \
            self._connector.place_and_execute(serialized_method_call_request)
        code, function_return = remote.decode_call_response(response)
        self.assertIn("/impossible_dir", function_return.split(":"))
    
    def test_set_get_pwd_dir(self):
        self.assertEqual(self._connector.get_pwd_dir(),
                 self._connector.get_home_dir())

        self._connector.set_pwd_at_home_dir("subfolder")
        self.assertEqual(self._connector.get_pwd_dir(),
                         self._connector.get_home_dir()+"/subfolder")
                
        self._connector.set_pwd_dir("/oneroute")
        self.assertEqual(self._connector.get_pwd_dir(), "/oneroute")
        
    
    def _configure_remote_environment(self):
        self._connector.set_sremote_dir("/tmp/sremote_test/")
        self._connector.set_tmp_dir("/tmp/sremote_test/")
        
        client = RemoteClient(self._connector)
        
        self.assertTrue(client.do_bootstrap_install())
    
def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__));

def create_file(route, content):
    orig_file = file(route, "w")
    orig_file.write(content)
    orig_file.close()
    

        
    
