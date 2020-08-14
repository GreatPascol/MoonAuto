# -*- coding: utf-8 -*-
# @Time        : 2020/7/8 11:50
# @Author      : Pan
# @Description : 
import functools


class A(object):
    a = 'sdf'
    def __init__(self):
        self.__s = "xxx"
        self.__msg = "hi"

    def record_msg(self, name):
        print(self.__msg, " ", name)

    @staticmethod
    def log(text, bbb):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(text, bbb)
                # self.record_msg('aaa')
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def fun(self):
        """sdfsdfsd"""
        print(self.__s)


a = A()
print(a.fun.__name__)
for attr in dir(a.fun):
    print(attr, getattr(a.fun, attr))
a.fun()
print(a.a)
