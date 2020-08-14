# -*- coding: utf-8 -*-
# @Time        : 2020/7/29 18:15
# @Author      : Pan
# @Description : 
import abc


class Element(object):
    @abc.abstractclassmethod
    def exist(self):
        pass
