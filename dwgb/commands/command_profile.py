from .command_custom import cmd_custom
from datetime import *

class command_profile(cmd_custom):

    FIELD_PROFILE = 'profile'

    def validate(self, message):
        tmpMatch = self.getMatch(r'^\[id(\d+)\|(.+?)].+Бездна \((\d+)\).+подземелья: (\d+).+👊(\d+) 🖐(\d+) ❤(\d+) 🍀(\d+) 🗡(\d+) 🛡(\d+)', message.text)
        return tmpMatch
    
    def work(self, message, data):
        if (message.user != self.DW_ID):
            return True
        tmpText = ''
        tmpNow = datetime.today()
        tmpParams = dict()
        tmpParams['elite'] = int(data[3]) 
        tmpParams['level'] = int(data[4]) 
        tmpParams['power'] = int(data[5]) 
        tmpParams['speed'] = int(data[6]) 
        tmpParams['hp'] = int(data[7]) 
        tmpParams['funny'] = int(data[8])
        tmpParams['attack'] = int(data[9])
        tmpParams['defend'] = int(data[10])
        tmpParams['date'] = tmpNow.timestamp()
        tmpSnapshot = self.database.getParam(data[1], self.FIELD_PROFILE)
        if tmpSnapshot == None:
            tmpSnapshot = tmpParams
            self.saveData(data[1], data[2], tmpSnapshot, tmpParams, True, message)
        elif (tmpNow - datetime.fromtimestamp(tmpSnapshot['date'])).days > 7:
            self.saveData(data[1], data[2], tmpSnapshot, tmpParams, True, message)
        else:
            self.saveData(data[1], data[2], tmpSnapshot, tmpParams, False, message)
        return True

    def saveData(self, id, name, snapshot, params, save, message):
        if save:
            self.database.setParam(id, self.FIELD_PROFILE, params)
            tmpText = '🏁 Реестр обновлен. '
            tmpTime = -1
        else:
            tmpText = ''
            tmpTime = 0        
        tmpText += self.getAccountTag(int(id), name) + ', последний учет: ' + datetime.fromtimestamp(snapshot['date']).strftime('%Y.%m.%d %H:%M') + ' \n'
        tmpText += self.getBlock('☠', params['elite'], snapshot['elite'])
        tmpText += self.getBlock('🎄', params['level'], snapshot['level'])
        tmpText += self.getBlock('👊', params['power'], snapshot['power'])
        tmpText += self.getBlock('🖐', params['speed'], snapshot['speed'])
        tmpText += self.getBlock('❤', params['hp'], snapshot['hp'])
        tmpText += self.getBlock('🍀', params['funny'], snapshot['funny'])
        tmpText += self.getBlock('🗡', params['attack'], snapshot['attack'])
        tmpText += self.getBlock('🛡', params['defend'], snapshot['defend'])
        self.transport.writeChannel(tmpText, message, False, tmpTime)
        return

    def getBlock(self, icon, newValue, oldValue):
        tmpValue = newValue - oldValue
        tmpText = icon + str(newValue)
        if (tmpValue > 0):
            tmpText += '(+' + str(tmpValue) + ')'
        elif (tmpValue < 0):
            tmpText += '(' + str(tmpValue) + ')'
        return tmpText + ' '