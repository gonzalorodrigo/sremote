
import client_api
import newt_connector
from sys import argv

print argv
connector = newt_connector.ClientNewtConnector(argv[1])
client_api.connector = connector

if not connector.auth(argv[2], password=argv[3]):
    print "Error auth!"
    exit()


client_api.qsummary()