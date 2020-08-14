# -*- coding: utf-8 -*-
# @Time        : 2020/7/12 11:49
# @Author      : Pan
# @Description :

from tkinter import Button, E, W, NW, X, Label, TOP, LEFT, Frame, BOTH, PhotoImage
from ...core.commander.impl.browser import PageElement
from ..editor.models import CommandMetadata, ParamMetadata, CommandModel, ParamMetadata, ParamMetadata
from ..editor.views import ParamView, EntryParamView, BoolParamView, TextParamView
from ...tool.chrome_inspect import ChromeInspector
from ..common.image import ImageWrapper
from moonauto.gui import tk_helper


class PluginPageElement(PageElement):
    def __init__(self, image_data, *args):
        super().__init__(*args)
        self.image_data = image_data


class PageElementParamView(ParamView):
    def refresh_value(self, value):
        pass

    def init_ui(self, desc, value):
        self.image_wrapper = ImageWrapper()
        if value is None:
            value = PageElement('', '', '')
        e_name = value.name
        e_xpath = value.xpath
        e_img_path = value.screenshot_path

        head_frame = Frame(self)
        head_frame.pack(side=TOP, anchor=NW)
        content_frame = Frame(self, borderwidth=1)
        content_frame.pack(side=TOP, expand=True, fill=BOTH)

        Label(head_frame, text=desc+"： ", justify="center").pack(side=LEFT, anchor=NW)
        Button(head_frame, text='选择元素', command=self.choose_element).pack(side=LEFT, anchor=W)
        self.element_name_view = EntryParamView(content_frame)
        self.element_name_view.init_ui('元素名', e_name)
        self.element_name_view.pack(anchor=W, pady=5, padx=20)
        self.element_xpath_view = TextParamView(content_frame)
        self.element_xpath_view.init_ui('xpath', e_xpath)
        self.element_xpath_view.pack(anchor=W, pady=5, padx=20)
        self.img_label = Label(content_frame)
        self.img_label.pack(expand=True, fill=BOTH, pady=5, padx=20)
        if hasattr(value, 'image_data'):
            self.img_label.configure(image=value.image_data)

    def _load_image_by_data(self, data):
        self.image_tk = self.image_wrapper.load_from_bytes(data).get_tk_image(150)
        self.img_label.configure(image=self.image_tk)

    def _load_image_by_file_path(self, file_path):
        self.image_tk = self.image_wrapper.load_from_file(file_path).get_tk_image(150)
        self.img_label.configure(image=self.image_tk)

    def get_value_from_view(self):
        e_name = self.element_name_view.get_value_from_view()
        e_xpath = self.element_xpath_view.get_value_from_view()
        return PluginPageElement(self.image_tk, e_name, e_xpath, self.image_wrapper.file_path)

    def choose_element(self):
        def f():
            ChromeInspector().set_select_hook()
            tk_helper.tk_state_normal()
            e = ChromeInspector().current_selected_element
            self.element_name_view.refresh_value(e[0])
            self.element_xpath_view.refresh_value(e[1])
            self._load_image_by_data(e[2])
        ChromeInspector().set_select_hook(f)
        ChromeInspector().start_inspect()
        tk_helper.tk_state_icon()


COMMAND_TEMPLATE_LIST = []


def set_template():
    global COMMAND_TEMPLATE_LIST
    COMMAND_TEMPLATE_LIST.extend([
        CommandMetadata('输入文本', 'input', [
            ParamMetadata('操作元素', 'element', PageElementParamView),
            ParamMetadata('输入文本', 'text', EntryParamView),
            ParamMetadata('是否最后输入Enter键', 'send_enter_key', BoolParamView, False)
        ]),
        CommandMetadata('点击', 'click', [
            ParamMetadata('操作元素', 'element', PageElementParamView),
        ]),
        CommandMetadata('双击', 'double_click', [
            ParamMetadata('操作元素', 'element', PageElementParamView),
        ]),
        CommandMetadata('打开地址', 'navigate', [
            ParamMetadata('网址', 'url', EntryParamView),
        ]),
        CommandMetadata('切换到标签', 'switch_to_tab', [
            ParamMetadata('标签id', 'tab_id', EntryParamView),
        ]),
        CommandMetadata('确认alert框', 'alert_accept', [
            ParamMetadata('输入文本', 'input_text', EntryParamView),
        ] ),
        CommandMetadata('忽略alert框', 'alert_dismiss', [

        ]),
    ])


