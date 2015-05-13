import qdo_remote_api_sim

client = qdo_remote_api_sim.QDORemoteClient(
            qdo_remote_api_sim.QDOLocalConnector("edison"))
client.qsummary()