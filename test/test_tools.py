"""UNIT TESTS for sremote helping tools.


 python -m unittest test_tools
 
"""

import json
import pkg_resources
import sremote.tools as remote
import unittest
import os

class TestTools(unittest.TestCase):


    def setUP(self):
        pass
    
    def test_call_method_object_command(self):
        self.assertEqual(remote.call_method_object_command(
                                          {remote.COMMAND_MODULE:"test_tools",
                                           remote.COMMAND_TYPE:"mock_function",
                                           remote.COMMAND_ARGS:["1", "2"]
                                          }),
                         "12")
    
    def test_call_method_object(self):
        
        self.assertEqual(remote.call_method_object("test_tools",
                                                   "mock_function",
                                                   ["1", "2"]),
                        "12")
        
        
        self.assertEqual(remote.call_method_object("test_tools", 
                                                   "mock_function",
                                                   {"arg1":"2", "arg2":"3"}),
                         "23")
        with self.assertRaises(remote.ExceptionRemoteExecError):
            remote.call_method_object("non_existing_module",
                                                    "method", [])
        with self.assertRaises(remote.ExceptionRemoteExecError):
            remote.call_method_object("test_tools", "non_existing_method", [])
        with self.assertRaises(remote.ExceptionRemoteExecError):
            remote.call_method_object("test_tools", "exception_raiser", [])
  
    def test_set_environ_variables(self):
        remote.set_environ_variables({"MYVAR":"MYVAL"})
        self.assertEqual(os.getenv("MYVAR", None), "MYVAL")
        remote.set_environ_variables({"MYVAR":"MYVALCHANGED", 
                                      "MYVAR2":"MYVAL2"})
        self.assertEqual(os.getenv("MYVAR", None), "MYVALCHANGED")
        self.assertEqual(os.getenv("MYVAR2", None), "MYVAL2")
        remote.set_environ_variables({"MYVAR":"MYVALCHANGEDAGAIN", 
                                      "MYVAR3":"MYVAL3"}, True)
        self.assertEqual(os.getenv("MYVAR", None), "MYVALCHANGED")
        self.assertEqual(os.getenv("MYVAR3", None), "MYVAL3")
    
    def test_add_environ_path(self):
        self.assertNotIn("/myPath", os.getenv("PATH").split(":"))
        self.assertNotIn("/myOtherPath", os.getenv("PATH").split(":"))
        remote.add_environ_path(["/myPath", "/myOtherPath"])
        self.assertIn("/myPath", os.getenv("PATH").split(":"))
        self.assertIn("/myOtherPath", os.getenv("PATH").split(":"))
        
    def test_process_remote_call(self):
                
        ret_values=remote.process_remote_call("""
        {"module": "test_tools", "command": "env_check", 
        "args": ["MYVAR", "HOME", "PATH"], "modules_check": ["os"], 
        "enviroment_variables": {"MYVAR":"MYVAL"},
        "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
        "path_addons" : ["/mypath"]
        }
        """)
        self.assertEqual(ret_values[0], "MYVAL")
        self.assertNotEqual(ret_values[1], "HOMEMODIFIED")
        self.assertIn("/mypath", ret_values[2])
        
        ret_values=remote.process_remote_call("""
        {"module": "test_tools", "command": "env_check",
        "args": {"var1": "MYVAR", "var2":"HOME", "var3": "PATH"},
        "modules_check": ["os"], 
        "enviroment_variables": {"MYVAR":"MYVAL"},
        "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
        "path_addons" : ["/mypath"]
        }
        """)
        self.assertEqual(ret_values[0], "MYVAL")
        self.assertNotEqual(ret_values[1], "HOMEMODIFIED")
        self.assertIn("/mypath", ret_values[2])
        
        with self.assertRaises(remote.ExceptionRemoteExecError):
            ret_values=remote.process_remote_call("""
                {"module": "FAILMODULE", "command": "env_check",
                "args": {"var1": "MYVAR", "var2":"HOME", "var3": "PATH"},
                "modules_check": ["os"], 
                "enviroment_variables": {"MYVAR":"MYVAL"},
                "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
                "path_addons" : ["/mypath"]
                }
                """)
        
        with self.assertRaises(remote.ExceptionRemoteExecError):
            ret_values=remote.process_remote_call("""
                {"module": "test_tools", "command": "env_check",
                "args": {"var1": "MYVAR", "var2":"HOME", "var3": "PATH"},
                "modules_check": ["os", "FAILMODULE"], 
                "enviroment_variables": {"MYVAR":"MYVAL"},
                "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
                "path_addons" : ["/mypath"]
                }
                """)
        
    def test_encode_call_request(self):
        self.assertEqual(json.loads(remote.encode_call_request(
                        module_name="test_tools", command_name="env_check",
                         args = ["MYVAR", "HOME", "PATH"], 
                        required_extra_modules = ["os"],
                        remote_env_variables = {"MYVAR":"MYVAL"},
                        conditional_remote_env_variables = {"HOME":
                                                            "HOMEMODIFIED"},
                        remote_path_addons = ["/mypath"])),
                    json.loads("""{"module": "test_tools", 
                    "command": "env_check", 
                    "args": ["MYVAR", "HOME", "PATH"], "modules_check": ["os"], 
                    "enviroment_variables": {"MYVAR":"MYVAL"},
                    "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
                    "path_addons" : ["/mypath"]
                    }"""))
    
    def test_decode_call_request(self):
        self.assertEqual(remote.decode_call_request(
                    """{"module": "test_tools", 
                    "command": "env_check", 
                    "args": ["MYVAR", "HOME", "PATH"], "modules_check": ["os"], 
                    "enviroment_variables": {"MYVAR":"MYVAL"},
                    "conditional_enviroment_variables": {"HOME":"HOMEMODIFIED"},
                    "path_addons" : ["/mypath"]
                    }"""),
                    (
                     "test_tools", 
                    "env_check", 
                    ["MYVAR", "HOME", "PATH"], 
                    ["os"], 
                    {"MYVAR":"MYVAL"},
                    {"HOME":"HOMEMODIFIED"},
                    ["/mypath"]) 
                    )
    def test_encode_call_response(self):
        self.assertEqual(json.loads(remote.encode_call_response("RETURN VALUE",
                                                     True, 
                                                     ["sremote"] )),
                         json.loads(
                         """{"return_value" : "RETURN VALUE",
                              "success": true,
                              "sremote_version": """+
                              _quote(_get_module_version("sremote"))+ """,
                              "modules_check": 
                              {"sremote": """+
                                _quote(_get_module_version("sremote"))+
                            """}}"""))
    
    def test_decode_call_response(self):
        self.assertEqual(remote.decode_call_response(
                        """{"return_value" : "RETURN VALUE",
                              "success": true,
                              "sremote_version": """+
                              _quote(_get_module_version("sremote"))+ """,
                              "modules_check": 
                              {"sremote": """+
                                _quote(_get_module_version("sremote"))+
                            """}}"""),
                          (True,
                           "RETURN VALUE"
                           ))
                         
    def test_check_modules_versions(self):
        old_get_module_version= remote.get_module_version
        old_module_exists = remote.module_exists
        remote.get_module_version = _fake_get_module_version
        remote.module_exists = _fake_module_exists
        
        self.assertTrue(remote.check_modules_versions({"MODULE1": "1.0",
                                                       "MODULE2": "2.0"}))
        with self.assertRaises(remote.ExceptionRemoteModulesError):
            remote.check_modules_versions({"MODULE1": "1.0", "MODULE2": "3.0"})
        with self.assertRaises(remote.ExceptionRemoteModulesError):
            remote.check_modules_versions({"MODULE3": "1.0", "MODULE2": "3.0"})
        
        remote.get_module_version=old_get_module_version 
        remote.module_exists=old_module_exists
            
    def test_parse_location_file(self):
        text = """
            {"sremote": "/tmp/sremote_test/selfd",
            "absolute_tmp": "/tmp/sremote_test/tmp",
            "absolute_pwd": "/tmp/sremote_test/pwd"
            }
        """
        location = remote.parse_location_file(text)
        self.assertEqual(location["sremote"], "/tmp/sremote_test/selfd")
        self.assertEqual(location["absolute_tmp"], "/tmp/sremote_test/tmp")
        self.assertEqual(location["absolute_pwd"], "/tmp/sremote_test/pwd")
        
        text = """
            {"sremote": "/tmp/sremote_test/selfd",
            "relative_tmp": "tmp",
            "relative_pwd": "pwd"
            }
        """
        location = remote.parse_location_file(text)
        self.assertEqual(location["sremote"], "/tmp/sremote_test/selfd")
        self.assertEqual(location["relative_tmp"], "tmp")
        self.assertEqual(location["relative_pwd"], "pwd")
        
        text = """
            {"sremote": "/tmp/sremote_test/selfd"
            }
        """
        self.assertFalse(remote.parse_location_file(text))
        
        text = """
            {relative_tmp": "tmp"
            }
        """
        self.assertFalse(remote.parse_location_file(text))
        text = """
            {relative_tmp": "tmp" asdas das d
            }
        """
        self.assertFalse(remote.parse_location_file(text))
        
def _fake_get_module_version(module_name):
    if (module_name == "MODULE1"):
        return "1.0"
    elif (module_name == "MODULE2"):
        return "2.0"
    return 0.0

def _fake_module_exists(module_name):
    if (module_name == "MODULE1"):
        return True
    elif (module_name == "MODULE2"):
        return True
    return False
    
def _quote(cad):
    return "\""+cad+"\""
def _get_module_version(module_name):
    return str(pkg_resources.get_distribution(module_name).version)
def mock_function(arg1=None, arg2=None):
    return arg1+arg2

def env_check(var1, var2, var3):
    values = []
    values.append(os.getenv(var1, None))
    values.append(os.getenv(var2, None))
    values.append(os.getenv(var3, None))
    return values

def exception_raiser():
    raise Exception, "Hi! from the method!"