# -*- coding: utf-8 -*-
from tkinter import Listbox, Scrollbar, Frame, Menu, Text, Canvas, RIGHT, LEFT, BOTH, X, Y, BOTTOM, HORIZONTAL, Pack, Grid, Place, StringVar, Entry
from tkinter.ttk import Treeview


class BaseWindow(Frame):
    def __init__(self, title):
        super().__init__()
        self.master.title(title)
        self.menu_bar = Menu(self)
        self._head_menu_dict = {}
        self.master.config(menu=self.menu_bar)
        self._topmost = False

    def add_menu_bar_command(self, head, label, command, accelerator=''):
        m = self._head_menu_dict.get(head)
        if m is None:
            m = Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label=head, menu=m)
            self._head_menu_dict[head] = m
        m.add_command(label=label, command=command, accelerator=accelerator)
        return m

    def center_window(self, w, h):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.master.geometry('%dx%d+%d+%d' % (w, h, (sw - w)/2, (sh - h)/2))

    def toggle_topmost(self):
        if self._topmost:
            self.master.wm_attributes('-topmost', 0)
        else:
            self.master.wm_attributes('-topmost', 1)
        self._topmost = not self._topmost




class ScrolledListbox(Listbox):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        super().__init__(self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Listbox).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def get_cur_select_index(self):
        return self.curselection()[0] if len(self.curselection()) != 0 else -1


class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))


class ScrolledCanvas(Canvas):
    def __init__(self, master=None, x=True, y=True, **kw):
        #
        self.__base_frame = Frame(master)  # scrollbar and canvas both slave to this base_frame
        if x:
            self._hbar = Scrollbar(self.__base_frame, orient=HORIZONTAL)
            self._hbar.pack(side=BOTTOM, fill=X)
            kw.update({'xscrollcommand': self._hbar.set})
            self._hbar['command'] = self.xview
        if y:
            self._vbar = Scrollbar(self.__base_frame)
            self._vbar.pack(side=RIGHT, fill=Y)
            kw.update({'yscrollcommand': self._vbar.set})
            self._vbar['command'] = self.yview
        Canvas.__init__(self, self.__base_frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Canvas).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.__base_frame, m))
