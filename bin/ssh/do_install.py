
import sremote.api as remote
import sremote.connector.ssh as ssh
from sys import argv


connector = ssh.ClientSSHConnector("127.0.0.1")
connector.auth("gonzalo")

client = remote.RemoteClient(connector)

output = connector.execute_command("pwd")
print output



if not connector.copy_file("./file.txt", "~/file.txt"):
    print "error copying file"



output  = connector.execute_command("ls")
print output




