
import sremote.api as remote
import sremote.connector.ssh as ssh
from sys import argv


connector = ssh.ClientSSHConnector("hopper.nersc.gov")
connector.auth("gprodri")

client = remote.RemoteClient(connector)

client.do_bootstrap_install()
 
client.do_install_git_module(
             "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git", 
             "master")