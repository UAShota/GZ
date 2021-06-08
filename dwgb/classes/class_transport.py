from .class_message import bot_message
from vkapi.longpoll import *
from vkapi import *
from datetime import *
import vkapi
import traceback

class bot_transport(object):
    """ Структура описания передачи предмета или золота """

    #: Блок удаления сообщений
    TAG_SERVER = 'server'

    #: Блок удаления сообщений
    TAG_DELETE_MSG = 'messages'

    #: Блок TS сервера
    TAG_SERVER_TS = 'ts'

    def __init__(self, database, token, ownerId):
        """ Конструктор """
        self.database = database
        self.token = token
        self.ownerId = ownerId
        self.client = VkApi(token = self.token)
        self.poll = VkLongPoll(self.client)

    def getOwnerId(self):
        """ Идентификатор бота """
        return self.ownerId

    def getName(self, id, data):
        """ Возвращение имени отправителя из расширенных полей сообщения """
        if id < 0:
            tmpField = 'groups'
        else:
            tmpField = 'profiles'
        for tmpItem in data[tmpField]:
            if tmpItem['id'] == abs(id):
                if id < 0:
                    return tmpItem['name']
                else:
                    return tmpItem['first_name'] + ' ' + tmpItem['last_name']
        return id

    def timePassed(self, msgTimeStamp):
        """ Проверка истекания времени жизни сообщения """
        return datetime.today().timestamp() - msgTimeStamp >= 60

    def readEvents(self, events):
        """ Запрос параметров сообщения из расширенных полей сообщения """
        tmpMessages = set()
        tmpData = self.poll.preload_message_events_data(events, 1)
        for tmpEvent in events:
            try:
                tmpMessage = bot_message()
                tmpMessage.id = tmpEvent.message_id
                tmpMessage.channel = tmpEvent.peer_id
                if tmpEvent.from_group:
                    tmpMessage.user = -tmpEvent.group_id
                else:
                    tmpMessage.user = tmpEvent.user_id
                tmpMessage.name = self.getName(tmpMessage.user, tmpData)
                tmpMessage.text = tmpEvent.text
                tmpMessages.add(tmpMessage)
            except:
                print(tmpMessage.id)  
                print(tmpMessage.user)
                print(tmpData)
        print('.', end='', flush=True)
        return tmpMessages

    def readChannels(self):
        """ Итерация чтения каналов """
        self.poll.ts = self.database.getInt(self.TAG_SERVER, self.TAG_SERVER_TS)
        self.clearChannel()  
        tmpEvents = set()        
        try:            
            for tmpEvent in self.poll.check():
                if (tmpEvent.type == VkEventType.MESSAGE_NEW):
                    tmpEvents.add(tmpEvent)
            if tmpEvents:
                yield self.readEvents(tmpEvents)              
        except:
            traceback.print_exc()
            pass
        self.database.setParam(self.TAG_SERVER, self.TAG_SERVER_TS, self.poll.ts)

    def writeChannel(self, text, message, reply, lifetime=0):
        """ Отправка сообщения """
        tmpParams = {
            'peer_id': message.channel,
            'message': text,
            'random_id': 0
        }
        if reply:
            tmpParams.update({'reply_to': message.id})
        tmpId = self.client.method('messages.send', tmpParams)
        if lifetime >= 0:
            self.database.setParam(self.TAG_DELETE_MSG, str(tmpId), datetime.today().timestamp() + lifetime)

    def clearChannel(self):
        """ Очистка оставленных сообщений """
        tmpDeleting = set()
        tmpMessages = self.database.getArray(self.TAG_DELETE_MSG)
        for tmpMessage in tmpMessages:
            if self.timePassed(tmpMessages[tmpMessage]):
                tmpDeleting.add(tmpMessage)
        if not tmpDeleting:
            return
        tmpParams = {
            'message_ids': ','.join(str(tmpId) for tmpId in tmpDeleting),
            'delete_for_all': 1
        }
        try:
            self.client.method('messages.delete', tmpParams)
        except:
            pass
        for tmpDeleted in tmpDeleting:
            tmpMessages.pop(tmpDeleted)
        self.database.setArray(self.TAG_DELETE_MSG, tmpMessages)