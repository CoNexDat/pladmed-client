class CommandManager:
    def __init__(self, command, validator=None):
        self.command = command
        self.validator = validator
    
    def validate(self, param):
        if self.validator is not None:
            self.validator.validate(param)

    def parse_command(self, param):
        return self.command + " " + str(param)

class MultiCommandManager(CommandManager):
    def parse_command(self, param):
        complete_param = self.command + " "

        for sub_param in param:
            complete_param += str(sub_param) + " "

        return complete_param.rstrip()
