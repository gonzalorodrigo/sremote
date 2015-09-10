
import os
import sremote.tools as remote
from sremote.api import RemoteClient

import unittest


class TestRemoteClient(unittest.TestCase):
    """Abstract class to define unittests for specific implementations"""
    
    
    def setUp(self):
        self._connector = self.create_connector()
        self._client=RemoteClient(self._connector)
    
    def create_connector(self):
        return None
    
    def test_do_remote_call(self):
        self._configure_remote_environment()
        self._client.register_remote_env_path("/mypath")
        response, stdout= self._client.do_remote_call(module_name="os",
                                                      method_name="getenv", 
                                                      args=["PATH"])
        
        self.assertIn("/mypath", response)
        
        self._client.register_remote_env_variable("MYVAR", "VALUE1")
        response, stdout= self._client.do_remote_call(module_name="os",
                                                      method_name="getenv", 
                                                      args=["MYVAR"])
        
        self.assertEqual("VALUE1", response)
        
        self._client.register_remote_env_variable("PATH", "VALUE1", True)
        response, stdout= self._client.do_remote_call(module_name="os",
                                                      method_name="getenv", 
                                                      args=["PATH"])
        
        self.assertNotEqual("VALUE1", response)
        
        with self.assertRaises(remote.ExceptionRemoteExecError):
            response, stdout= self._client.do_remote_call(
                                                    module_name="kkk",
                                                    method_name="getenv",
                                                    args=["PATH"])
        
        with self.assertRaises(remote.ExceptionRemoteExecError):
            response, stdout= self._client.do_remote_call(
                                                    module_name="os",
                                                    method_name="kkk",
                                                    args=["PATH"])
        
    
    def test_do_install_git_module(self):
        self._configure_remote_environment()
        self.assertTrue(self._client.do_install_git_module(
                                "https://bitbucket.org/berkeleylab/qdo.git",
                                "remote", keep_after="mydir"))
        self._client.register_remote_module("qdo")
        response, stdout= self._client.do_remote_call(module_name="qdo.remote",
                                                      method_name="get_version")
        self.assertIn("0.", response)
        
        self.assertTrue(self._connector.retrieve_file(
                                    "/tmp/sremote_test/tmp/mydir/README.md", 
                                    "/tmp/README.md"))
        
    def test_register_remote_module_negative(self):
        #- Positive is tested in test_do_install_git_module
        self._configure_remote_environment()
        self._client.register_remote_module("kkk")
        with self.assertRaises(remote.ExceptionRemoteModulesError):
            response, stdout= self._client.do_remote_call(
                                                    module_name="os",
                                                    method_name="getenv",
                                                    args=["PATH"])
        
    def test_get_resource_route(self):
        route=self._client.get_resource_route("interpreter.sh")
        self.assertTrue(os.path.isfile(route))
        
    def _configure_remote_environment(self):
        self._connector.set_sremote_dir("/tmp/sremote_test")
        self._connector.set_tmp_dir("/tmp/sremote_test")        
        self.assertTrue(self._client.do_bootstrap_install())