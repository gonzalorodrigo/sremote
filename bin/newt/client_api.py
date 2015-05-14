"""Resulting remoted module. This is the version of remote_api that is executed
in the client code.It includes the creation of the connector and the the
invocation of the remote classes.
"""


import sremote.api as remote_api

_remote_module = "remote_api"
connector = None

    
def qsummary():
    client = remote_api.RemoteClient(connector)
    
    return_value = client.do_remote_call(_remote_module, "qsummary")
    print return_value
    
