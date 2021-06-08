from .command_custom import cmd_custom

class command_convert(cmd_custom):
    
    def validate(self, message):
        tmpMatch = self.getMatch(r'^чистыми (\d+)$', message.text)
        return tmpMatch
    
    def work(self, message, data):
        tmpValue = int(data[1])
        self.transport.writeChannel(data[1] + ' чистыми ' + str(tmpValue + round(tmpValue / 9)), message, False)
        return True