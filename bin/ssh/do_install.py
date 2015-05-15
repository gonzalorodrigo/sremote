
import sremote.api as remote
import sremote.connector.ssh as ssh
from sys import argv


connector = ssh.ClientSSHConnector("127.0.0.1")
connector.auth("gonzalo")

client = remote.RemoteClient(connector)

client.do_bootstrap_install()
 
client.do_install_git_module(
             "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git", 
             "master")


# 
# 
# def do_bootstrap_install(connector, install_dir):
#     connector.execute_command("mkdir", ["-p", install_dir])
#     if not connector.push_file("./setup_bootstrap.sh", 
#                                "~/"+install_dir+"/setup_bootstrap.sh"):
#         print "Error placing installation script."
#         return False
#     if not connector.push_file("./interpreter.sh", 
#                            "~/"+install_dir+"/interpreter.sh"):
#         print "Error placing interpreter script"
#         return False
#     output, err, rc = connector.execute_command("/bin/csh", 
#                         ["~/"+install_dir+"/setup_bootstrap.sh"])
#     print "Install result:", rc, output, err
#     return True
# 
# do_bootstrap(connector)




