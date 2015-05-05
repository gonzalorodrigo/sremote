
import qdo_remote_api as remote

import newt_lib as newt


 ### cmd = "python -c 'import qdo; print [q.summary() for q in qdo.qlist()]' "


def qsummary():
    out, err, stats = send_command("hopper", "qsummary")
    print out
    response = remote.decode_call_response(out)
    print response


def send_command(host, command_type, args = []):
    newt_client = newt.NewtClient()
    std_out, err_out, status = newt_client.place_and_execute(
                                "./interpreter.sh",
                                remote.encode_call_request(command_type,
                                 args))
    
    return std_out, err_out, status
qsummary()