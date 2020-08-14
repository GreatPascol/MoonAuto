# -*- coding: utf-8 -*-
# @Time        : 2020/7/9 21:01
# @Author      : Pan
# @Description : 

from moonauto.gui.editor.main import CommandEditor
from moonauto.gui.tk_helper import get_tk_root

root = get_tk_root()
app = CommandEditor("自动脚本录制工具")
app.center_window(600, 700)
app.toggle_topmost()
root.mainloop()
