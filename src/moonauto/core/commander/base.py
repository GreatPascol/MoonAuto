# -*- coding: utf-8 -*-
# @Time        : 2020/6/24 17:09
# @Author      : Pan
# @Description : 
import abc
from .info import CommanderInfo


class BaseCommander(object):
    def __init__(self):
        self.__commander_info = None

    def set_commander_info(self, commander_info: CommanderInfo):
        self.__commander_info = commander_info

    def record_msg(self, msg):
        if self.__commander_info:
            self.__commander_info.add_msg(msg)

    def record_img(self, img_data, img_ext):
        if self.__commander_info:
            self.__commander_info.add_img(img_data, img_ext)

    @abc.abstractmethod
    def close(self):
        pass


