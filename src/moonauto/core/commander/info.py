# -*- coding: utf-8 -*-
# @Time        : 2020/7/17 11:39
# @Author      : Pan
# @Description : 
import abc
import sys
import time


class AbstractCommanderInfoObserver(object):
    @abc.abstractmethod
    def notify(self, msg):
        pass


class CommanderInfo(object):
    def __init__(self):
        self.__msgs = []
        self.__imgs = []
        self.__observers = []

    @property
    def msgs(self):
        return self.__msgs

    @property
    def imgs(self):
        return self.__imgs

    def register(self, observer):
        self.__observers.append(observer)

    def notify(self, msg):
        for o in self.__observers:
            o.notify(msg)

    def add_msg(self, msg, with_datetime=True):
        if with_datetime:
            msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '' + msg
        self.__msgs.append(msg)
        self.notify(msg)

    def add_img(self, data, ext):
        self.__imgs.append(img)


class FileObserver(AbstractCommanderInfoObserver):
    def __init__(self, stream=sys.stdout, ln='\n'):
        self._stream = stream
        self._ln = ln

    def notify(self, msg):
        self._stream.write(msg)
        self._stream.write(self._ln)
