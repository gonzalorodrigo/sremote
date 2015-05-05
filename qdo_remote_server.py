import sys
import qdo
import qdo_remote_api as remote

if (sys.argv):
    file_route = sys.argv[1]
    text_file = open(file_route, "r")
    content = "\n".join(text_file.readlines())
    command_name, args = remote.decode_commnad(content)
    #print "COMMMMAND", command_name
    reponse_obj = remote.call_method_object(qdo, command_name, args)
    print remote.encode_response(reponse_obj, True)
else:
    print remote.encode_response({}, False)