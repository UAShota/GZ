from .command_custom import cmd_custom
from classes import bot_transfer

class transferitem(cmd_custom):
    
    def validate(self, message):        
        tmpMatch = self.getMatch(r'^👝\[id(\d+)\|(.+?)], получено: (.+?)(, )?(\d+)?( штук)? от игрока \[id(\d+)\|(.+?)]', message.text)
        return tmpMatch
    
    def incomingFree(self, transfer):
        tmpHave = self.database.getInt(transfer.sourceId, transfer.type)
        self.database.setParam(transfer.sourceId, transfer.type, tmpHave + transfer.count)
        self.transport.writeChannel(self.getAccountTag(transfer.targetId, transfer.targetName) + ', ' + transfer.type + ' взято на хранение', transfer.message, False)
        return True
    
    def outDoorFree(self, transfer):
        tmpHave = self.database.getInt(transfer.targetId, transfer.type)
        self.database.setParam(transfer.targetId, transfer.type, tmpHave - transfer.count)
        self.transport.writeChannel(self.getAccountTag(transfer.sourceId, transfer.sourceName) + ', ' + str(transfer.count) + ' ' + transfer.type + ' взято с хранения', transfer.message, False)
        return True

    def work(self, message, data):
        if (message.user != self.DW_ID):
            return True
        tmpTransfer = bot_transfer()
        tmpTransfer.message = message
        tmpTransfer.sourceId = int(data[1])
        tmpTransfer.sourceName = data[2]
        tmpTransfer.type = data[3].lower()
        if data[5] != None:
            tmpTransfer.count = int(data[5])
        else:
            tmpTransfer.count = 1
        tmpTransfer.targetId = int(data[7])
        tmpTransfer.targetName = data[8]
        tmpTransfer.item = self.findItem(tmpTransfer.type)
        if tmpTransfer.sourceId == self.transport.getOwnerId():
            return self.incomingFree(tmpTransfer)
        if tmpTransfer.targetId == self.transport.getOwnerId():
            return self.outDoorFree(tmpTransfer)
        return False