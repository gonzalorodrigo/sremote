"""UNIT TESTS for the ServerChannel class


python -m unittest test_server_channel

"""


from sremote.api import ServerChannel
import sremote.tools as remote
import test_connector
import unittest


class TestServerChannel(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_process_call_request(self):
        request = remote.encode_call_request("os",
                                           "getenv",
                                           ["MYVAR"],
                                           [],
                                           {"MYVAR": "VALUE1"},
                                           {}, 
                                           [])
        test_connector.create_file("/tmp/sremote_test/request.data", request)
        server = ServerChannel()
        return_content=server.process_call_request(
                                    "/tmp/sremote_test/request.data",
                                     "/tmp/sremote_test/response.data")
        file_response = open("/tmp/sremote_test/response.data")
        response_content = file_response.read()
        
        self.assertEqual(return_content, response_content)
        
        status, reponse_obj = remote.decode_call_response(response_content)
        self.assertEqual(reponse_obj, "VALUE1")
        
    
    def test_process_call_request_exceptions(self):
        
        request = remote.encode_call_request("test_server_channel",
                                           "raiser_function",
                                           ["MYVAR"],
                                           [],
                                           {"MYVAR": "VALUE1"},
                                           {}, 
                                           [])
        test_connector.create_file("/tmp/sremote_test/request.data", request)
        server = ServerChannel()
        return_content=server.process_call_request(
                                    "/tmp/sremote_test/request.data",
                                     "/tmp/sremote_test/response.data")
        file_response = open("/tmp/sremote_test/response.data")
        response_content = file_response.read()       
        status, reponse_obj = remote.decode_call_response(response_content)
        self.assertFalse(status)
        
        self.assertEqual(reponse_obj["sremote_type"], 
                         "ExceptionRemoteExecError")
        
        
        request = remote.encode_call_request("test_server_channel",
                                           "non_exist",
                                           ["MYVAR"],
                                           [],
                                           {"MYVAR": "VALUE1"},
                                           {}, 
                                           [])
        test_connector.create_file("/tmp/sremote_test/request.data", request)
        server = ServerChannel()
        return_content=server.process_call_request(
                                    "/tmp/sremote_test/request.data",
                                     "/tmp/sremote_test/response.data")
        file_response = open("/tmp/sremote_test/response.data")
        response_content = file_response.read()       
        status, reponse_obj = remote.decode_call_response(response_content)
        self.assertFalse(status)
        
        self.assertEqual(reponse_obj["sremote_type"], 
                         "ExceptionRemoteExecError")
        
        
        
def raiser_function(in_value):
    raise Exception("Hi!")
        
    
    
     
