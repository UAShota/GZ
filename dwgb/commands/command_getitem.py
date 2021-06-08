from .command_custom import cmd_custom

class getitem(cmd_custom):

    def validate(self, message):
        tmpMatch = self.getMatch(r'^хочу (\d+)?(\D+)', message.text)
        return tmpMatch

    def getItem(self, message, type, item, count):
        count = min(count, self.database.getInt(self.transport.getOwnerId(), type))
        if count <= 0:
            self.transport.writeChannel('👝 ' + type + ' нет в наличии', message, False)
            return True
        if item == None:
            self.transport.writeChannel('Передать ' + type + ' - ' + str(count) + ' штук', message, True)
            return True
        self.transport.writeChannel('Передать ' + item.id + ' - ' + str(count) + ' штук', message, True)
        return True
    
    def work(self, message, data):
        if data[1] != None:
            tmpCount = int(data[1])
        else:
            tmpCount = 1
        tmpType = data[2].strip().lower()
        tmpItem = self.findItem(tmpType)
        if tmpItem != None:
            tmpType = tmpItem.id
        return self.getItem(message, tmpType, tmpItem, tmpCount)