

import subprocess


class NewtClient:

    def __init__(self, hostname="hopper"):
        self._hostnamm = hostname

    def place_and_execute(self, content):
        command = "./interpreter.sh"
        location = self.place_string_as_file(content)
        return self.execute_command(command, location)

    def execute_command(self, command, arg):
        p = subprocess.Popen([command, arg], stdout=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        return output, err, rc

    def place_string_as_file(self, content, file_route=None):
        if file_route == None:
            file_route = self.gen_random_file_route()
        text_file = open(file_route, "w")
        text_file.write(content)
        text_file.close()
        return file_route

    def gen_random_file_route(self):
        return "file_name.dat"
