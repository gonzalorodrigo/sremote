import remote_api
import subprocess
import requests

_interpreter_route = "~/qdo_interpreter/qdo_interpreter_newt.sh"


class QDONewtConnector(remote_api.CommsChannel):

    """
    Base class for the client side of the remoting functions


    """

    def __init__(self, hostname="hopper"):
        self._hostname = hostname
        self._token = None

    def auth(self, username, password=None, token=None):
        self._username = username
        if password:
            data = dict(
                username=username,
                password=password,
            )    
            url = "https://newt.nersc.gov/newt/auth/"
            results = requests.post(url, data)
            if results.status_code == 200:
                res_obj = results.json()
                newt_sessionid = res_obj['newt_sessionid']
                self._token = newt_sessionid
                del res_obj['newt_sessionid']
                del results
                return True
            else:
                del results
                self._token = None
                return False
        else:
            self._token = token

    def execute_request(self, arg):
        """Uses NEWT to run a command on the requested NERSC host
        """
        cmdurl = "https://newt.nersc.gov/newt/command/" + self._hostname
        qdo_authkey = self._token

        data = dict(
            executable=_interpreter_route+" "+arg,
            loginenv='true',
        )
    
        results = requests.post(cmdurl, data,
                                cookies={'newt_sessionid': qdo_authkey})

        output =  results.json()["output"]
        del results
        return output, "", 0


    def place_call_request(self, content, file_route=None):
        """Uses NEWT to upload a file
        """
        if file_route == None:
            file_route = self.gen_random_file_route()
        
        cmdurl = ("https://newt.nersc.gov/newt/file/"+ self._hostname
                  + file_route)

        qdo_authkey = self._token

        data = bytearray(content)
        results = requests.put(cmdurl, data,
                               cookies={'newt_sessionid': qdo_authkey})
        if (results.status_code == 200):
            del results
            return file_route
        else:
            del results
            return False


    def gen_random_file_route(self):
        base = "/global/u1/"+self._username[0]+"/"+self._username+"/.qdo/"
        return base+"file_name.dat"

    def retrieve_call_request(self, content_pointer):
        text_file = open(content_pointer, "r")
        content = "\n".join(text_file.readlines())
        return content
