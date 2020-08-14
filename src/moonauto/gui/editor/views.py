# -*- coding: utf-8 -*-
# @Time        : 2020/7/9 19:47
# @Author      : Pan
# @Description :
import abc
import threading
from tkinter import *
from tkinter.ttk import Frame, Button, Label, LabelFrame, Combobox, Entry, Notebook

from ..common.widgets import ScrolledListbox, ScrolledText, ScrolledCanvas
from .models import ParamModel


class ParamView(Frame):
    """composite pattern"""
    def __init__(self, parent, param_model=None):
        super().__init__(parent)
        self._param_model = param_model

    def update_model(self):
        if self._param_model is not None:
            self._param_model.value = self.get_value_from_view()

    @abc.abstractmethod
    def init_ui(self, desc, value):
        pass

    @abc.abstractmethod
    def get_value_from_view(self):
        pass

    @abc.abstractmethod
    def refresh_value(self, value):
        pass


class EntryParamView(ParamView):
    def get_value_from_view(self):
        text = self.entry.get()
        return text

    def init_ui(self, desc, value):
        if value is None:
            value = ''
        Label(self, text=desc+"： ", justify="center").pack(side=LEFT, anchor=NW)
        self.entry = Entry(self)
        self.entry.pack(side=LEFT, padx=5)
        self.entry.insert(0, value)

    def refresh_value(self, value):
        self.entry.delete(0, END)
        self.entry.insert(0, value)


class BoolParamView(ParamView):
    def get_value_from_view(self):
        checked = self._var.get()
        return checked

    def init_ui(self, desc, value):
        if value is None:
            value = False
        self._var = BooleanVar(self, value=value)
        Label(self, text=desc+"： ", justify="center").pack(side=LEFT, anchor=NW)
        Checkbutton(self, text='', variable=self._var, onvalue=True, offvalue=False).pack(side=LEFT, anchor=W, padx=5, fill=X)

    def refresh_value(self, value):
        self._var.set(value)


class TextParamView(ParamView):
    def get_value_from_view(self):
        text = self.text.get(1.0, END)
        return text

    def init_ui(self, desc, value):
        if value is None:
            value = ''
        Label(self, text=desc+"： ", justify="center").pack(side=LEFT, anchor=NW)
        self.text = ScrolledText(self, height=2, width=20)
        self.text.pack(side=LEFT)
        self.text.insert(1.0, value)

    def refresh_value(self, value):
        self.text.delete(1.0, END)
        self.text.insert(1.0, value)


