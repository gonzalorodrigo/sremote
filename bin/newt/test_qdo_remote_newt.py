
import qdo_remote_api_newt
from sys import argv

print argv

connector = qdo_remote_api_newt.QDONewtConnector(argv[1])
client = qdo_remote_api_newt.QDORemoteClient(
            connector)
if not connector.auth(argv[2], password=argv[3]):
    print "Error auth!"
    exit()


client.qsummary()