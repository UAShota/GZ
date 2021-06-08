import os.path
import json

class bot_database(object):
    """ Управление БД бота """

    def __init__(self, dataPath):
        """ Конструктор """
        self.fileName = dataPath + 'database.txt'
        self.load()

    def __del__(self):
        """ Деструктор """
        self.save()

    def load(self):
        """ Загрузка БД из файла """
        if (os.path.isfile(self.fileName)):
            with open(self.fileName, 'r', encoding = 'utf-8') as tmpFile:
                self.config = json.load(tmpFile)
        else:
            self.config = {}

    def save(self):
        """ Сохранение БД в файл """
        with open(self.fileName, 'w', encoding = 'utf-8') as tmpFile:
            json.dump(self.config, tmpFile, ensure_ascii = False)

    def setParam(self, node, tag, value):
        """ Установка одного параметра """
        tmpNode = str(node)
        if not tmpNode in self.config:
            self.config[tmpNode] = { tag: value }
        else:
            self.config[tmpNode][tag] = value

    def setArray(self, node, value):
        """ Установка массива параметра """
        tmpNode = str(node)
        self.config[tmpNode] = value

    def getInt(self, node, tag):
        """ Возвращение числового значения параметра  """
        tmpNode = str(node)
        if tmpNode in self.config:
            if tag in self.config[tmpNode]:
                return int(self.config[tmpNode][tag])
        return 0

    def getParam(self, node, tag):
        """ Возвращение числового значения параметра  """
        tmpNode = str(node)
        if tmpNode in self.config:
            if tag in self.config[tmpNode]:
                return self.config[tmpNode][tag]
        return None

    def getArray(self, node):
        """ Возвращение словаря параметров """
        tmpNode = str(node)
        if tmpNode in self.config:
            return self.config[tmpNode]
        else:
            return {}