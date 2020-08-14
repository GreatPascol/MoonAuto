# -*- coding: utf-8 -*-
# @Time        : 2020/6/24 17:09
# @Author      : Pan
# @Description : 
import abc
from moonauto.util.clazz_util import SingletonMetaClass


class CommanderFactory(metaclass=SingletonMetaClass):

    def create(self):
        commander = self._new_commander()

        return commander

    @abc.abstractmethod
    def _new_commander(self):
        pass
