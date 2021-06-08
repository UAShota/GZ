from .command_custom import cmd_custom

class baf(cmd_custom):

    CMD_ACTION = 'action'
    CMD_MATCH = 'match'
    CMD_BAF = 'baf'

    def useBaf(self, message, data):
        self.transport.writeChannel('Благословение ' + data[1], message, True)
        return True

    def validate(self, message):
        tmpResult = {}
        tmpMatch = self.getMatch(r'^хочу баф (.+)', message.text)
        if tmpMatch != None:
            tmpResult[self.CMD_MATCH] = tmpMatch
            tmpResult[self.CMD_ACTION] = self.CMD_BAF
            return tmpResult
        else:
            return False

    def work(self, message, data):
        if data[self.CMD_ACTION] == self.CMD_BAF:
            return self.useBaf(message, data[self.CMD_MATCH])
        else:
            return False