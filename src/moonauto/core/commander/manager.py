# -*- coding: utf-8 -*-
# @Time        : 2020/6/24 17:10
# @Author      : Pan
# @Description :
from .info import CommanderInfo, FileObserver
from .factory import CommanderFactory
from moonauto.util.clazz_util import SingletonMetaClass


def get_default_commander_info():
    ci = CommanderInfo()
    ci.register(FileObserver())
    return ci


class CommanderManager(metaclass=SingletonMetaClass):
    def __init__(self):
        self.__commanders = {}
        self._commander_info = None

    def get_commander(self, factory: CommanderFactory, commander_id=""):
        if commander_id not in self.__commanders:
            c = factory.create()
            c.set_commander_info(self._commander_info)
            self.__commanders[commander_id] = c
        return self.__commanders[commander_id]

    def remove_commander(self, commander_id):
        c = self.__commanders.pop(commander_id)
        c.close()

    def update_commander_info(self, commander_info: CommanderInfo):
        self._commander_info = commander_info
        for c in self.__commanders.values():
            c.set_commander_info(commander_info)

    def clean(self):
        for c in self.__commanders.values():
            c.close()
        self.__commanders.clear()

