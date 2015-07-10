"""Implementation of the sremote.api.ClientChannel class that uses Newet as
the communication channel. Newt is a REST api to interact with the NERSC
systems."""

import sremote.api as remote_api
import requests

class ClientNEWTConnector(remote_api.ClientChannel):

    
    def __init__(self, hostname, interpreter_route = "interpreter.sh"):
        self._interpreter_route = interpreter_route
        self._hostname = hostname;
        self._token = None
    
    
    def auth(self, username, password=None, token=None, home_dir=None):
        """Auth method. It performs auth operation against the newt server and
        stores the token for futher use. It also detects the users login dir
        and stores it.

        Args:
            username: string with user to be auth as. It is stored for future
            operations.
            password: string, if set, the auth process is executed and token
            retrieved. Token is stored for further operations.
            token: string, if password not set, this value is stored as the
            token for future operations.

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
                    if home_dir:
                        self._home_dir = home_dir 
                    else:
                        self._home_dir = self.get_pwd()
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
            if home_dir:
                self._home_dir = home_dir 
            else:
                self._home_dir = self.get_pwd()
            print self._home_dir
            if self._home_dir!=None:
                return True
            else:
                return False
        
    
    def status(self):
        """Returns true if the self._token is valid and the code can login."""
        cmdurl = "https://newt.nersc.gov/newt/login/"
        qdo_authkey = self._token

        results = requests.get(cmdurl, cookies={'newt_sessionid': qdo_authkey})

        ok_auth = results.json()["auth"]
        del results
        return ok_auth

    def push_file(self, origin_route, dest_route):

        cmdurl = ("https://newt.nersc.gov/newt/file/" + self._hostname
                  + dest_route)

        qdo_authkey = self._token
        text_file = open(origin_route, "r")
        results = requests.put(cmdurl, text_file,
                               cookies={'newt_sessionid': qdo_authkey})
        text_file.close()
        if (results.status_code == 200):
            del results
            return True
        else:
            del results
            return False
    
    def retrieve_file(self, origin_route, dest_route):
        
        cmdurl = ("https://newt.nersc.gov/newt/file/" + self._hostname
                  + origin_route +"?view=read")

        qdo_authkey = self._token
        text_file = open(dest_route, "w")
    
        results = requests.get(cmdurl, text_file,
                               cookies={'newt_sessionid': qdo_authkey})
        text_file.writelines(results)
        text_file.close()
        if (results.status_code == 200):
            del results
            return True
        else:
            del results
            return False

        
    def execute_command(self, command, arg_list=[], keep_env=False):
        cmdurl = "https://newt.nersc.gov/newt/command/" + self._hostname
        qdo_authkey = self._token

        data = dict(
            executable=" ".join([command]+arg_list),
            loginenv='false',
        )
        if keep_env:
            data['loginenv'] = 'true'
        #print data
        
        results = requests.post(cmdurl, data,
                                cookies={'newt_sessionid': qdo_authkey})
        #print results
        output = results.json()["output"]
        error = results.json()["error"]
        del results
        return output, error, 0
    
    def get_home_dir(self):
        return self._home_dir




