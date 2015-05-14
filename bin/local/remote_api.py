"""This is an example of an API that is going to be remoted. client_api is 
the resulting remoted module called by the client code.

"""

import qdo

def qsummary(user=None, worker=None):
    """
    Return a list of dictionaries with the state of known queues

    Optional inpluts:
        user    : name of user who owns this queue (default $USER)
        worker  : name of worker connecting to these queues
    """
    return [q.summary() for q in qdo.qlist()]