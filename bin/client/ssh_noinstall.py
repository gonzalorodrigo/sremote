"""Example of client code to execute the method valid_queue_name
of the QDO module on a remote systems (sremote and qdo
configured). It uses SSH as the communication connector.

Invocation:
python newt.py full_hostname username password
"""

import sremote.api as remote
import sremote.connector.ssh as ssh
from sremote.tools import ExceptionRemoteExecError, ExceptionRemoteModulesError
import time
from sys import argv


def valid_queue_name(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", args=[value])
    run_time = time.time()-start_t
    print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

def valid_queue_name_dict(value):

    start_t = time.time()
    return_value, out = client.do_remote_call("qdo", "valid_queue_name", 
                                              args={"name":value})
    run_time = time.time()-start_t
    print out
    print "Total Execution time of call valid_queue_name (s):", run_time
    return return_value

def exception_trigger(value):

    try:
        return_value, out = client.do_remote_call("random_module",
                                                  "valid_queue_name", 
                                                  args={"name":value})
    except ExceptionRemoteModulesError as e:
        print "Exception to be raised, module does not exist: "+str(e)
        
    try:
        return_value, out = client.do_remote_call("qdo", "random_method", 
                                              args={"name":value})
    except ExceptionRemoteExecError as e:
        print "Exception to be raised, method does not exist: "+str(e)
       
    try: 
        return_value, out = client.do_remote_call("qdo", "connect", 
                                              args={"queue_name":"random_queue"}
                                              )
    except ExceptionRemoteExecError as e:
        print "Exception to be raised, ValueError: "+str(e)  
        

def setting_remote_var():
    client.register_remote_env_variable("myVar", "myValue")
    client.register_remote_env_variable("HOME", "This not", only_if_no_set=True)
    client.register_remote_env_variable("HOME_B", "This YES", only_if_no_set=True)
    
    
    return_value, out = client.do_remote_call("os", "getenv", 
                                              args=["HOME"]
                                              )
    
    print "HOME", return_value
    return_value, out = client.do_remote_call("os", "getenv", 
                                              args=["myVar"]
                                              )
    print "They should be the same value",  return_value, "myValue"
    
    return_value, out = client.do_remote_call("os", "getenv", 
                                              args=["HOME_B"]
                                              )
    print "HOME_B", return_value
    
        


#
# client.do_bootstrap_install()
#
# client.do_install_git_module(
#              "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git")
#
# import sremote.api as remote_api
connector = ssh.ClientSSHConnector(argv[1])
connector.set_sremote_dir("/tmp/sremote")
connector.set_tmp_at_home_dir("/qdo_private")
connector.auth(argv[2])

client = remote.RemoteClient(connector)


setting_remote_var()

exit()

print valid_queue_name("juanito")
print valid_queue_name_dict("juanito!")

exception_trigger("juanito")
