from .command_custom import cmd_custom

class storage(cmd_custom):

    CI_MAX = 76
    CMD_ACTION = 'action'
    CMD_MATCH = 'match'
    CMD_GET = 1
    CMD_SET = 2

    def validate(self, message):
        tmpResult = {}
        tmpMatch = self.getMatch(r'^хочу склад$', message.text)
        if tmpMatch != None:
            tmpResult[self.CMD_MATCH] = tmpMatch
            tmpResult[self.CMD_ACTION] = self.CMD_GET
            return tmpResult
        tmpMatch = self.getMatch(r'^склад (\d+) (.+)$', message.text)
        if tmpMatch != None:
            tmpResult[self.CMD_MATCH] = tmpMatch
            tmpResult[self.CMD_ACTION] = self.CMD_SET
            return tmpResult
        return False

    def work(self, message, data):
        if data[self.CMD_ACTION] == self.CMD_GET:
            return self.useGet(message, data[self.CMD_MATCH])
        if data[self.CMD_ACTION] == self.CMD_SET:
            return self.useSet(message, data[self.CMD_MATCH])
        return False
    
    def useGet(self, message, data):
       tmpParams = self.database.getArray(self.transport.getOwnerId())
       tmpData = ''
       tmpHave = 0
       for tmpName, tmpCount in sorted(tmpParams.items()):
            if tmpCount <= 0:
                continue
            tmpItem = self.findItem(tmpName)
            tmpHave += tmpCount
            if tmpItem:
                if tmpItem.short:
                    tmpShort = ' (' + tmpItem.short + ')'
                else:
                    tmpShort = ''
                tmpData += '🛒' + tmpItem.id.capitalize() + ': ' + str(tmpCount) + tmpShort + '\r\n'
            else:
                tmpData += '🛒' + tmpName.capitalize() + ': ' + str(tmpCount) + ' без цены\r\n'
       if tmpHave == 0:
           tmpData = '📦Склад пустой :('
       else:
           tmpData = '📦Заполненность склада: ' + str(tmpHave) + ' из ' + str(self.CI_MAX) + '\r\n' + tmpData
       self.transport.writeChannel(tmpData, message, False, 60)
       return True
   
    def useSet(self, message, data):
        self.database.setParam(self.transport.getOwnerId(), data[2], int(data[1]))
        self.transport.writeChannel("Записано " + data[1] + " для " + data[2], message, True)
        return True