# -*- coding: utf-8 -*-
# @Time        : 2020/6/29 11:36
# @Author      : Pan
# @Description :
import threading


class SingletonMetaClass(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonMetaClass._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instance
