from classes import *
from commands import *
import os
import traceback
import time

class bot_engine(object):
    """ Движок обработки команд """
        
    def __init__(self, dir, token, owner, channels):
        """ Конструктор """
        self.datapath = dir + '/data/'
        if not os.path.isdir(self.datapath):
            os.mkdir(self.datapath)
        self.datapath = dir + '/data/' + str(owner) + '/'
        if not os.path.isdir(self.datapath):
            os.mkdir(self.datapath)
        self.database = bot_database(self.datapath)
        self.transport = bot_transport(self.database, token, owner)
        self.commands = {}
        self.channels = channels
        self.registerCommands()

    def registerCommand(self, name, classType):
        """ Регистрация команды """
        self.commands[name] = classType(self.database, self.transport)

    def registerCommands(self):
        """ Регистрация доступных команд """
        self.registerCommand(bot_consts.COMMAND_SAVEPROFILE, command_profile)
        self.registerCommand(bot_consts.COMMAND_STORAGE, storage)
        self.registerCommand(bot_consts.COMMAND_TRANSFERITEM, transferitem)
        self.registerCommand(bot_consts.COMMAND_GETBAF, baf)
        self.registerCommand(bot_consts.COMMAND_GETITEM, getitem)
        self.registerCommand(bot_consts.COMMAND_CONVERT, command_convert)

    def exec(self, command, message):
        """ Выполнение команды для сообщения """
        try:
            tmpCall = self.commands[command]
            tmpMatch = tmpCall.validate(message)
            if not tmpMatch:
                return False
            elif command in self.channels[message.channel]:
                return tmpCall.work(message, tmpMatch)
            else:
                return True
        except:
            traceback.print_exc()
            pass

    def check(self, messages):
        """ Проверка сообщений для выполнения """
        for tmpMessage in messages:
            if not tmpMessage.channel in self.channels:
                continue
            for tmpCmd in self.commands:
                if self.exec(tmpCmd, tmpMessage):
                    break

    def listen(self):
        """ Проверка сообщений для выполнения """
        tmpReadChannels = self.transport.readChannels
        while True:
            for tmpMessages in tmpReadChannels():
                self.check(tmpMessages)
                self.database.save()
                time.sleep(1)