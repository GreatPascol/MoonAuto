# -*- coding: utf-8 -*-
# @Time        : 2020/8/13 12:07
# @Author      : Pan
# @Description : 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


__driver = None


def detect_driver():
    if __driver is None:
        return False
    return True


def get_driver(port=9222):
    if not detect_driver():
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--remote-debugging-port=' + str(port))
        d = webdriver.Chrome(chrome_options=chrome_options, executable_path='lib/web/driver/chromedriver.exe')

        h = d.current_window_handle
        ws = d.window_handles[1:]
        for w in ws:
            d.switch_to.window(w)
            d.close()
        d.switch_to.window(h)
        d.get("http://cn.bing.com")
        global __driver
        __driver = d
    return __driver
