import qdo_remote_api_sim
import qdo_remote_api_newt
from sys import argv

print argv

connector = qdo_remote_api_newt.QDONewtConnector(argv[1])
client = qdo_remote_api_sim.QDORemoteClient(
            connector)
if not connector.auth("gprodri", password=argv[2]):
    print "Error auth!"
    exit()


client.qsummary()