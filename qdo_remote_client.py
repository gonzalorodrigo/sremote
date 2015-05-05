import remote_client
import qdo_local_connector as conn

class QDORemoteClient(remote_client.RemoteClient):
    def qsummary(self):
        return_value = self.do_remote_call("qsummary")
        print return_value


client = QDORemoteClient(conn.QDOLocalConnector("edison"))
client.qsummary()