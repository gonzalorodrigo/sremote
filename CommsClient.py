import subprocess


class CommsClient:
    """
    Base class for the client side of the remoting functions


    """

    def place_and_execute(self, content):
        location = self.place_call_request(content)
        return self.execute_request(location)

    def execute_request(self, arg):
        raise Exception("Non implemented")

    def place_call_request(self, content, file_route=None):
        raise Exception("Non implemented")

