import qdo_remote_api_sim
import qdo_remote_api_newt

connector = qdo_remote_api_newt.QDONewtConnector("hopper")
client = qdo_remote_api_sim.QDORemoteClient(
            connector)
if not connector.auth("gprodri", ""):
    print "Error auth!"
    exit()


client.qsummary()