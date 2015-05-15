
import sremote.api as remote
import sremote.connector.newt as newt
from sys import argv


connector = newt.ClientNEWTConnector(argv[1])
if not connector.auth(argv[2], argv[3]):
    print "Auth error", argv[2], argv[3]
    exit()

client = remote.RemoteClient(connector)

client.do_bootstrap_install()
 
client.do_install_git_module(
             "https://gonzalorodrigo@bitbucket.org/berkeleylab/qdo.git", 
             "master")