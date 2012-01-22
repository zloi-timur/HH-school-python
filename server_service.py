import re

class CommandsParser():
    def __init__(self):
        self.commands = dict()

    def put_command(self, command):
        self.commands[command[0]] = re.compile(command[1])

    def parse(self, input_command):
        for com in self.commands.keys():
            if re.match(self.commands[com], input_command):
                return com, re.match(self.commands[com], input_command).groups()
        return None
