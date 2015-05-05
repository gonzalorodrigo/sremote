import remote_client
import newt_lib as newt

class QDORemoteClient(remote_client.RemoteClient):
    def qsummary(self):
        return_value = self.do_remote_call("qsummary")
        print return_value


client = QDORemoteClient(newt.NewtClient("edison"))
client.qsummary()