# -*- coding: utf-8 -*-
# @Time        : 2020/7/6 11:50
# @Author      : Pan
# @Description : 
import pychrome
import base64
from io import BytesIO, StringIO
from PIL import Image


print('xxx')
# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:9222")
print('xxx')
# list all tabs (default has a blank tab)
tabs = browser.list_tab()

if not tabs:
    tab = browser.new_tab()
else:
    tab = tabs[0]

# tab.debug = True

tab.start()

# tab.Network.enable()
# tab.Page.navigate(url="https://cn.bing.com", _timeout=5)

highlightConfig = {"showInfo": False, "showRulers": False, "showStyles": False, "showExtensionLines": False,
                   "contentColor": {"r": 111, "g": 168, "b": 220, "a": 0.66},
                   "paddingColor": {"r": 147, "g": 196, "b": 125, "a": 0.55},
                   "borderColor": {"r": 255, "g": 229, "b": 153, "a": 0.66},
                   "marginColor": {"r": 246, "g": 178, "b": 107, "a": 0.66},
                   "eventTargetColor": {"r": 255, "g": 196, "b": 196, "a": 0.66},
                   "shapeColor": {"r": 96, "g": 82, "b": 177, "a": 0.8},
                   "shapeMarginColor": {"r": 96, "g": 82, "b": 127, "a": 0.6},
                   "cssGridColor": {"r": 75, "g": 0, "b": 130}}


def element_inspect_event_callback(**kwargs):
    backend_node_id = kwargs['backendNodeId']
    print(backend_node_id)
    ret = tab.DOM.pushNodesByBackendIdsToFrontend(backendNodeIds=[backend_node_id])
    node_id = ret['nodeIds'][0]
    desc = tab.DOM.describeNode(nodeId=node_id, depth=-1)
    print(desc['node'])
    # data = tab.Page.captureScreenshot(clip={'x':2, 'y':2, 'width':300, 'height':400, 'scale':1})
    # image = Image.open(BytesIO(base64.b64decode(data['data'])))
    # image.show()


def print_node(node, steps=0):
    d = {}
    for k, v in node.items():
        if k != 'children':
            d[k] = v
    print(steps * ' ', d)
    for c in node.get('children', []):
        print_node(c, steps + 1)


def get_parent(node):
    if 'parentId' in node:
        desc = tab.DOM.describeNode(nodeId=node['parentId'], depth=0)
        print(desc)
        get_parent(desc)


tab.Overlay.inspectNodeRequested = element_inspect_event_callback
# tab.Overlay.nodeHighlightRequested = normal_event_callback
doc = tab.call_method("DOM.getDocument", depth=-1)
# print_node(doc['root'])
print(doc['root'])
tab.Page.enable()
tab.DOM.enable()
tab.CSS.enable()
tab.Overlay.enable()
tab.Console.enable()
tab.Overlay.setInspectMode(mode='searchForNode', highlightConfig=highlightConfig)


doc = tab.DOM.getDocument(depth=-1)
# tab.call_method("Overlay.disable")
# tab.call_method("Overlay.setInspectMode", mode='none', highlightConfig={})


# tab.wait(5)

# tab.stop()

# browser.close_tab(tab)
