# -*- coding: utf-8 -*-
# @Time        : 2020/8/9 21:13
# @Author      : Pan
# @Description :
import re

IDENTIFIER_ESCAPE_PATTERN = re.compile(r'[?\\/.,=+~!！？，。《》@#$%^&*()\-`<>;:"\'\[\]}{|（）\n]')


class TreeElement(object):
    """text是一种特殊节点"""
    def __init__(self, element_id, tag, *, parent=None, text=None, **attributes):
        self._element_id = element_id
        self._tag = tag
        self._parent = parent
        self._text = text
        self._attributes = attributes
        self._children = []

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return len(self._children) == 0

    def is_text(self):
        return self._text is not None

    @property
    def element_id(self):
        return self._element_id

    @property
    def tag(self):
        return self._tag

    @property
    def parent(self):
        return self._parent

    @property
    def attributes(self):
        return self._attributes

    def get_text(self):
        if self.is_text():
            return self._text
        text_list = []
        for child in self._children:
            text_list.append(child.get_text())
        return "".join(text_list)

    @property
    def children(self):
        return self._children

    def add_child(self, e):
        self._children.append(e)

    def siblings(self):
        """
        返回一个生成器，而不是占用实际内存和时间的list
        """
        return (c for c in self._parent.children if c.element_id != self._element_id)

    def find(self, e_id):
        if e_id == self._element_id:
            return self
        for child in self._children:
            result = child.find(e_id)
            if result is not None:
                return result
        return None

    def full_xpath(self):
        if self.is_root():
            return '/'
        for idx, e in self.siblings():
            if e.element_id == self._element_id:
                return '%s/%s[%d]' % (self._parent.full_xpath(), self._tag, idx)
        return '%s/%s' % (self._parent.full_xpath(), self._tag)


def __get_attr_counts(e: TreeElement, attr_value_counts):
    for a, v in e.attributes.items():
        if a not in attr_value_counts:
            attr_value_counts[a] = {}
        vc = attr_value_counts[a]
        vc[v] = 1 + vc.get(v, 0)
    for child in e.children:
        __get_attr_counts(child, attr_value_counts)


def get_repeat_attrs(root) -> list:
    attr_value_counts = {}
    __get_attr_counts(root, attr_value_counts)
    a_v_blacklist = {}
    for a, v_c in attr_value_counts.items():
        vs = []
        for v, c in v_c.items():
            if c > 1:
                vs.append(v)
        a_v_blacklist[a] = set(vs)
    return a_v_blacklist


class TreeAnalyzer(object):
    def __init__(self):
        self._root = None
        self._blacklist_attrs = ('class',)
        self._repeat_attr_value_pairs = {}
        self._special_attrs = ('name', 'id')

    def set_root(self, e: TreeElement):
        self._root = e
        self._repeat_attr_value_pairs = get_repeat_attrs(self._root)

    def __get_xpath_by_attr(self, tag, attr, v):
        if v != '' and v not in self._repeat_attr_value_pairs.get(attr, {}):
            return '//%s[@%s="%s"]' % (tag, attr, v)

    def get_xpath(self, e_id):
        e = self._root.find(e_id)
        if e is None:
            return ""
        for attr in self._special_attrs:
            v = e.attributes.get(attr, '')
            ret = self.__get_xpath_by_attr(e.tag, attr, v)
            if ret:
                return ret
        for attr, v in e.attributes.items():
            ret = self.__get_xpath_by_attr(e.tag, attr, v)
            if ret:
                return ret
        return e.full_xpath()

    @staticmethod
    def __get_desc_of_element(e):
        if e.tag == "input":
            t = e.attributes.get("placeholder", "").strip()
            if t != '':
                return t
        if e.tag == "frame":
            t = e.attributes.get("name", "").strip()
            if t != '':
                return t
        t = e.get_text()
        if t != '':
            return t
        t = e.attributes.get("title", "").strip()
        if t != '':
            return t
        t = e.attributes.get("value", "").strip()
        if t != '':
            return t
        return 'unknown_name'

    def get_identifier_name(self, e_id):
        e = self._root.find(e_id)
        if e is None:
            return ""
        desc = self.__get_desc_of_element(e)
        desc = re.sub(IDENTIFIER_ESCAPE_PATTERN, "", desc)
        return desc[:18].replace(" ", "_")
