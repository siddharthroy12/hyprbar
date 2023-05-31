import subprocess

# Run command and return output
def run_command(command):
    call_result = subprocess.run(command.split(" "), 
                                 stdout=subprocess.PIPE, 
                                 text=True)
    return call_result.stdout

# PUB/SUB
class Message:
    def __init__(self, initialValue):
        self._value = initialValue
        self.listiners = []

    def add_listener(self, callback):
        self.listiners.append(callback)
        callback(self._value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        for listiner in self.listiners:
            listiner(value)
        self._value = value
