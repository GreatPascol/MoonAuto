# -*- coding: utf-8 -*-
# @Time        : 2020/7/6 18:17
# @Author      : Pan
# @Description : 
import pychrome
from moonauto.util.clazz_util import SingletonMetaClass
from moonauto.core.analyzer.xhtml_tree import TreeElement, TreeAnalyzer
from moonauto.server.selenium_service import get_driver


HIGHLIGHT_CONFIG = {"showInfo": False, "showRulers": False, "showStyles": False, "showExtensionLines": False,
                     "contentColor": {"r": 111, "g": 168, "b": 220, "a": 0.66},
                     "paddingColor": {"r": 147, "g": 196, "b": 125, "a": 0.55},
                     "borderColor": {"r": 255, "g": 229, "b": 153, "a": 0.66},
                     "marginColor": {"r": 246, "g": 178, "b": 107, "a": 0.66},
                     "eventTargetColor": {"r": 255, "g": 196, "b": 196, "a": 0.66},
                     "shapeColor": {"r": 96, "g": 82, "b": 177, "a": 0.8},
                     "shapeMarginColor": {"r": 96, "g": 82, "b": 127, "a": 0.6},
                     "cssGridColor": {"r": 75, "g": 0, "b": 130}}

NORMAL_ATTR_LIST = ['id', 'name', 'class']


def describe_node(node):
    array = ['<%s-%s>' % (node['nodeName'], node['nodeType'])]
    attrs = node.get('attributes', [])
    attrs = dict(zip(attrs[::2], attrs[1::2]))
    for attr in NORMAL_ATTR_LIST:
        array.append("        %s: %s" % (attr, attrs.pop(attr, '')))
    for attr, v in attrs.items():
        array.append("        %s: %s" % (attr, v))
    return '\n'.join(array)


def get_chain_list(node, target_node_id):
    if node['backendNodeId'] == target_node_id:
        return [describe_node(node)]
    for child in node.get('children', []):
        sub_chain = get_chain_list(child, target_node_id)
        if sub_chain is not None:
            sub_chain.append(describe_node(node))
            return sub_chain
    return None


def parse_tree_element(node, parent=None):
    attrs = node.get('attributes', [])
    attrs = dict(zip(attrs[::2], attrs[1::2]))
    text = node['nodeValue'] if node['nodeType'] == 3 else None
    elem = TreeElement(node['backendNodeId'], node['localName'], parent=parent, text=text, **attrs)
    for child in node.get('children', []):
        elem.add_child(parse_tree_element(child, elem))
    return elem


class ChromeInspector(metaclass=SingletonMetaClass):
    def __init__(self, host='127.0.0.1', port=9222):
        self._port = port

        self._current_selected_element = None
        self._inspecting = False

        self._select_hook = None

        browser = pychrome.Browser(url="http://%s:%s" % (host, str(port)))

        tabs = browser.list_tab()
        for tab in tabs[1:]:
            browser.close_tab(tab)

        self.tab = tabs[0]
        self.tab.start()
        self.tab.Page.enable()
        self.tab.DOM.enable()
        self.tab.CSS.enable()
        self.tab.Overlay.enable()
        self.tab.Console.enable()

        self.tab.Overlay.inspectNodeRequested = self.element_inspect_event_callback
        self.doc = self.tab.DOM.getDocument(depth=-1)
        self._xpath_analyzer = TreeAnalyzer()

    def set_select_hook(self, f=None):
        self._select_hook = f

    def element_inspect_event_callback(self, **kwargs):
        backend_node_id = kwargs['backendNodeId']
        self.stop_inspect()
        self._current_selected_element = self.get_info_of_node(backend_node_id)
        if self._select_hook:
            self._select_hook()

    @property
    def current_selected_element(self):
        return self._current_selected_element

    @property
    def inspecting(self):
        return self._inspecting

    def start_inspect(self):
        if not self._inspecting:
            self.doc = self.tab.DOM.getDocument(depth=-1)
            self._xpath_analyzer.set_root(parse_tree_element(self.doc['root']))
            self.tab.call_method("Overlay.enable")
            self.tab.call_method("Overlay.setInspectMode", mode='searchForNode', highlightConfig=HIGHLIGHT_CONFIG)
            self._inspecting = True

    def stop_inspect(self):
        if self._inspecting:
            self.tab.call_method("Overlay.setInspectMode", mode='none', highlightConfig=HIGHLIGHT_CONFIG)
            self.tab.call_method("Overlay.disable")
            self._inspecting = False

    def get_info_of_node(self, node_id):
        xpath = self._xpath_analyzer.get_xpath(node_id)
        title = self._xpath_analyzer.get_identifier_name(node_id)
        return title, xpath, self.get_image_data_of_node(xpath)

    def get_image_data_of_node(self, xpath):
        e = get_driver().find_element_by_xpath(xpath)
        rect = e.rect
        rect['scale'] = 1
        data = self.tab.Page.captureScreenshot(clip=rect)
        return data['data']


if __name__ == '__main__':
    import sys
    sys.path.append('src')
    # ci = ChromeInspector()
    # ci.start_inspect()
    # import time
    # time.sleep(3600)
    # ci.stop_inspect()
