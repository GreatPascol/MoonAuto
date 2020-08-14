# -*- coding: utf-8 -*-
# @Time        : 2020/8/13 17:26
# @Author      : Pan
# @Description : 
from tkinter import Tk


GLOBAL_TK_ROOT = None


def get_tk_root():
    global GLOBAL_TK_ROOT
    GLOBAL_TK_ROOT = Tk()
    return GLOBAL_TK_ROOT


def tk_state_icon():
    GLOBAL_TK_ROOT.state('icon')


def tk_state_normal():
    GLOBAL_TK_ROOT.state('normal')
