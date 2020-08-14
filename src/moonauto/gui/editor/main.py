# -*- coding: utf-8 -*-
import functools
from tkinter import Tk, BOTH, Menu, BOTTOM, TOP, X, Y, RIGHT, LEFT, E, W, S, N, END, StringVar, BROWSE, Menu, NONE, ALL, ACTIVE
from tkinter.ttk import Frame, Button, Style, Label, LabelFrame, Combobox, Entry, Checkbutton, Notebook

from ..common.widgets import BaseWindow, ScrolledText, ScrolledListbox
from .components import CommandListView, ParamDisplayView, LogView
from ..plugins.browser_commander_plugin import COMMAND_TEMPLATE_LIST, set_template

from moonauto.core.commander.manager import CommanderManager, get_default_commander_info
from ...core.commander.impl.browser import BrowserCommanderFactory


class CommandEditor(BaseWindow):
    def __init__(self, title):
        super().__init__(title)
        # init_var
        self._browser_commander = None
        set_template()
        self.init_ui()

    def init_ui(self):
        # tab bar setting
        self.pack(fill=BOTH, expand=True)
        frame_main = Frame(self)
        frame_main.pack(fill=BOTH, expand=True, padx=5, pady=6)
        frame_4_log = LabelFrame(self, text="信息")
        frame_4_log.pack(fill=BOTH, expand=True, padx=5, pady=6)

        frame_4_commands = LabelFrame(frame_main, text="命令序列")
        frame_4_param = LabelFrame(frame_main, text="命令参数")
        frame_4_commands.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=6)
        frame_4_param.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=6)

        # first tab
        self.add_menu_bar_command("脚本", "打开", None)
        self.add_menu_bar_command("脚本", "保存", None)
        self.menu_plugin = self.add_menu_bar_command("插件", "打开浏览器", self.handler__open_browser, 'Crtl+b')
        # self.add_menu_bar_command("插件", "打开元素检查", self.handler__toggle_inspect, 'Crtl+a')
        self.add_menu_bar_command("插件", "录制模式", None, 'Crtl+r')
        self.add_menu_bar_command("帮助", "使用说明", None)
        self.add_menu_bar_command("帮助", "关于", None)

        self.menu_cmd = Menu(self.menu_bar, tearoff=0)
        for c in COMMAND_TEMPLATE_LIST:
            self.menu_cmd.add_command(label=c.desc, command=self.wrapper_handler__choose_cmd(c))

        self.cmd_list_view = CommandListView(frame_4_commands, self.menu_cmd)
        self.cmd_list_view.pack(side=TOP, expand=True, fill=BOTH)
        self.cmd_list_view.listbox__cmd_data.bind("<Double-Button-1>", self.handler__select_cmd)

        self._params_display_view = ParamDisplayView(frame_4_param, 300)
        self._params_display_view.pack(expand=True, fill=BOTH)
        Button(frame_4_param, text='保存修改', command=self._params_display_view.update_value).pack(anchor=E, padx=5, pady=5)

        self.log_view = LogView(frame_4_log)
        self.log_view.pack(expand=True, fill=BOTH)
        self._commander_info = get_default_commander_info()
        self._commander_info.register(self.log_view.commander_info_observer)
        CommanderManager().update_commander_info(self._commander_info)

    def handler__choose_cmd(self, cmd):
        command_model = cmd.new_command_model()
        self.cmd_list_view.add_cmd(command_model)
        self._params_display_view.load_params(command_model.param_models)

    def wrapper_handler__choose_cmd(self, cmd):
        def f():
            self.handler__choose_cmd(cmd)
        return f

    def handler__select_cmd(self, event):
        command_model = self.cmd_list_view.get_active_cmd()
        self._params_display_view.load_params(command_model.param_models)

    def handler__toggle_inspect(self):
        if self.browser_plugin.inspecting:
            self.menu_plugin.entryconfigure(1, label='打开元素检查')
            self.browser_plugin.stop_inspect()
        else:
            self.menu_plugin.entryconfigure(1, label='关闭元素检查')
            self.browser_plugin.start_inspect()

    def handler__open_browser(self):
        self._browser_commander = CommanderManager().get_commander(BrowserCommanderFactory())
