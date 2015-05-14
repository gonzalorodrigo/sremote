"""This is the NEWT specific remoting API. Developed for QDO, but can be used
with any code.

Definition of the comms channel:
    - The endpoint is a shell scripts in the user home directory.
    - All operations to use NEWT REST calls to invoke and interact with the
      end point.
    - The method call requests are sent to the end point as files that are
      stored in ~/.qdo/. References are file routes.
    - The channel require authentication one time. It retrieves a token that
      it kepts for subsequent operations in the same session. If the comms
      object is destroyed the session is lost.
    - If follows the NEWT Api spect at newt.nersc.gov
"""

import sremote.api as remote_api
import requests





class ClientNewtConnector(remote_api.ClientChannel):

    """Comms class to use remoting with NEWT
    """

    def __init__(self, hostname="hopper", 
                 interpreter_route = 
                    "/bin/csh ~/qdo_interpreter/bin/newt/interpreter.sh"):
        """Creation method, the destination machine is specified in hostname."""

        self._hostname = hostname
        self._token = None
        self._interpreter_route = interpreter_route

    def auth(self, username, password=None, token=None):
        """Auth method. It performs auth operation against the newt server and
        stores the token for futher use.

        Args:
            username: user to be auth as. It is stored for future operations.
            password: if set, the auth process is executed and token retrieved.
            Token is stored for further operations.
            token: if password not set, this value is stored as the token for
            future operations.

        Returns:
            True, if auth is successful.
        """
        self._username = username
        if password:
            data = dict(
                username=username,
                password=password,
            )
            url = "https://newt.nersc.gov/newt/auth/"
            results = requests.post(url, data)
            if results.status_code == 200:
                # We may get code 200, but still auth may have failed.
                res_obj = results.json()
                if (res_obj['auth']):
                    newt_sessionid = res_obj['newt_sessionid']
                    self._token = newt_sessionid
                    del res_obj
                    del results
                    return True
                del res_obj
                del results
                return False
            else:
                del results
                self._token = None
                return False
        else:
            self._token = token

    def status(self):
        """Checks if auth is successful"""
        cmdurl = "https://newt.nersc.gov/newt/login/"
        qdo_authkey = self._token

        results = requests.get(cmdurl, cookies={'newt_sessionid': qdo_authkey})

        ok_auth = results.json()["auth"]
        del results
        return ok_auth

    def execute_request(self, method_request_reference):
        """Executes a shell command in _hostname as _username to invoke
        the end point. It recives the methor request reference. 

        Args:
            method_request_reference: A file route pointing to a text file that
            contains the json serialized version of method request.

        Returns:
            string with whatever the endpoint produces on std output when
            executing the remote method.
        """
        cmdurl = "https://newt.nersc.gov/newt/command/" + self._hostname
        qdo_authkey = self._token

        data = dict(
            executable=self._interpreter_route + " " + method_request_reference,
            loginenv='true',
        )
        
        results = requests.post(cmdurl, data,
                                cookies={'newt_sessionid': qdo_authkey})

        output = results.json()["output"]
        error = results.json()["error"]
        del results
        return output, error, 0

    def place_call_request(self, serialized_method_call_request,
                           reference_route=None):
        """Places a request method call in the endpoint. It is uploaded as a
        file in the user's home directory.

        Args:
            serialized_method_call_request: serialized version of the request
            to be placed.
            reference_route: if set, where in the filesystem to place the 
            request.

        Returns:
            the filesystem route (absolute) where the request was placed.
        """
        if reference_route == None:
            reference_route = self.gen_random_file_route()

        cmdurl = ("https://newt.nersc.gov/newt/file/" + self._hostname
                  + reference_route)

        qdo_authkey = self._token

        data = bytearray(serialized_method_call_request)
        results = requests.put(cmdurl, data,
                               cookies={'newt_sessionid': qdo_authkey})
        if (results.status_code == 200):
            del results
            return reference_route
        else:
            del results
            return False

    def gen_random_file_route(self):
        base = "/global/u1/" + \
            self._username[0] + "/" + self._username + "/.qdo/"
        return base + "file_name.dat"

class ServerNewtConnector(remote_api.ServerChannel):   
    def retrieve_call_request(self, method_request_reference):
        text_file = open(method_request_reference, "r")
        content = "\n".join(text_file.readlines())
        return content
