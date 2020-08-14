# -*- coding: utf-8 -*-
# @Time        : 2020/7/10 17:19
# @Author      : Pan
# @Description :
import logging
import threading
from tkinter import Frame, Button, LEFT, W, E, TOP, BOTH, NONE, X, Y, END, messagebox, ACTIVE
from ..common.widgets import ScrolledCanvas, ScrolledListbox, ScrolledText
from moonauto.util import logUtil
from ...core.commander.impl.browser import BrowserCommanderFactory
from moonauto.core.commander.manager import CommanderManager

from moonauto.core.commander.info import AbstractCommanderInfoObserver


class ParamDisplayView(ScrolledCanvas):
    def __init__(self, parent, width, **kw):
        super().__init__(parent, x=False, **kw)
        self._frame = None
        self._width = width
        self._param_views = []
        self.init_ui()

    def init_ui(self):
        self._frame = Frame(self, width=self._width)
        self.create_window((0, 0), window=self._frame)
        self._frame.bind("<Configure>", self.handler__after_draw)

    def clear(self):
        for p in self._param_views:
            p.destroy()
        self._param_views.clear()

    def update_value(self):
        for p in self._param_views:
            p.update_model()

    def load_params(self, params):
        self.clear()
        for p in params:
            p_v = p.get_view(self._frame)
            self._param_views.append(p_v)
            p_v.pack(fill=X, padx=5, pady=10)

    def handler__after_draw(self, event=None):
        self.configure(scrollregion=self.bbox("all"))
        self.yview_moveto(0.0)
        self.xview_moveto(0.0)


class CommandListView(Frame):
    def __init__(self, parent, cmd_menu):
        super().__init__(parent)
        self.__command_model_list = []
        self._cmd_menu = cmd_menu
        #
        self._init_ui()

    def _init_ui(self):
        sub_frame__middle_control = Frame(self)
        sub_frame__middle_control.pack(side=LEFT, fill=Y)
        Button(sub_frame__middle_control, text="添加 ＋", command=self.handler__post_cmd_menu).pack(expand=True, fill=BOTH, padx=2, pady=3)
        Button(sub_frame__middle_control, text="上移 ↑", command=self.handler__move_up).pack(expand=True, fill=BOTH, padx=2, pady=3)
        Button(sub_frame__middle_control, text="下移 ↓", command=self.handler__move_down).pack(expand=True, fill=BOTH, padx=2, pady=3)
        Button(sub_frame__middle_control, text="删除 ×", command=self.handler__delete).pack(expand=True, fill=BOTH, padx=2, pady=3)
        Button(sub_frame__middle_control, text="运行 ►", command=self.handler__debug_rows_threaded).pack(expand=True, fill=BOTH, padx=2, pady=3)

        self.listbox__cmd_data = ScrolledListbox(self, width=20, height=13, font=("Consolas", "12"),
                                                 selectmode="extended", activestyle=NONE)
        self.listbox__cmd_data.pack(side=LEFT, expand=True, fill=BOTH)

    def add_cmd(self, cmd_model):
        self.listbox__cmd_data.insert(END, cmd_model.metadata.desc)
        self.__command_model_list.append(cmd_model)

    def get_active_cmd(self):
        cur_index = self.listbox__cmd_data.index(ACTIVE)
        cmd = self.__command_model_list[cur_index]
        return cmd

    def handler__delete(self):
        if not messagebox.askyesno("Warn", "确定删除所选行?"):
            return
        indexes = self.listbox__cmd_data.curselection()
        for i in range(len(indexes) - 1, -1, -1):
            if indexes[i] >= 0:
                self.listbox__cmd_data.delete(indexes[i])
                self.__command_model_list.pop(indexes[i])

    def handler__move_up(self):
        indexes = self.listbox__cmd_data.curselection()
        if len(indexes) == 0:
            return
        first = indexes[0]
        last = indexes[-1]
        if first == 0 or (last - first + 1) > len(indexes):
            return
        tmp_cmd_data = self.__command_model_list[first-1]
        for i in range(first-1, last):
            self.__command_model_list[i] = self.__command_model_list[i+1]
        self.__command_model_list[last] = tmp_cmd_data
        tmp_cmd_string = self.listbox__cmd_data.get(first-1)
        self.listbox__cmd_data.delete(first-1)
        self.listbox__cmd_data.insert(last, tmp_cmd_string)

    def handler__move_down(self):
        indexes = self.listbox__cmd_data.curselection()
        if len(indexes) == 0:
            return
        first = indexes[0]
        last = indexes[-1]
        if last == len(self.__command_model_list)-1 or (last - first + 1) > len(indexes):
            return
        tmp_cmd_data = self.__command_model_list[last+1]
        for i in range(last+1, first, -1):
            self.__command_model_list[i] = self.__command_model_list[i-1]
        self.__command_model_list[first] = tmp_cmd_data
        tmp_cmd_string = self.listbox__cmd_data.get(last+1)
        self.listbox__cmd_data.delete(last+1)
        self.listbox__cmd_data.insert(first, tmp_cmd_string)

    def handler__debug_rows(self):
        commander = CommanderManager().get_commander(BrowserCommanderFactory())
        indexes = self.listbox__cmd_data.curselection()
        for i in indexes:
            cmd_model = self.__command_model_list[i]
            cmd_model.run(commander)
        print('完成')

    def handler__debug_rows_threaded(self):
        threading.Thread(target=self.handler__debug_rows, daemon=True).start()

    def handler__post_cmd_menu(self):
        self._cmd_menu.post(self.winfo_rootx(), self.winfo_rooty())


class LogViewCommanderInfoObserver(AbstractCommanderInfoObserver):
    def __init__(self, log_view):
        super().__init__()
        self._log_view = log_view

    def notify(self, msg):
        self._log_view.log_msg(msg)


class LogView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._commander_info_observer = LogViewCommanderInfoObserver(self)

        self.txt_area__log = ScrolledText(self, height=10)
        self.txt_area__log.pack(expand=True, fill=BOTH)
        Button(self, text='清空日志', command=self.clear_log).pack(anchor=E, padx=5)
        self.txt_area__log.tag_configure(
            'title', font=('微软雅黑', 16, 'bold'),
            foreground='black', background='MediumSpringGreen', spacing3=20)
        self.txt_area__log.tag_configure(
            'error', foreground='red')
        self.txt_area__log.tag_configure(
            'highlight', background='whitesmoke')

    @property
    def commander_info_observer(self):
        return self._commander_info_observer

    def clear_log(self):
        self.txt_area__log.delete(1.0, END)

    def log_msg(self, msg):
        self.txt_area__log.insert(END, msg + "\n")

