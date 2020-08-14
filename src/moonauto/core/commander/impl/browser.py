# -*- coding: utf-8 -*-
# @Time        : 2020/7/8 16:29
# @Author      : Pan
# @Description : 
from ..base import BaseCommander
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..factory import CommanderFactory
from moonauto.server.selenium_service import get_driver


DEFAULT_WAIT_TIMEOUT = 20


class PageElement(object):
    def __init__(self, name, xpath, screenshot_path):
        self.name = name
        self.xpath = xpath
        self.screenshot_path = screenshot_path

    def __str__(self):
        return '<%s>' % self.name


class SeleniumHelper(object):
    def __init__(self, driver, wait_timeout=DEFAULT_WAIT_TIMEOUT):
        self._driver = driver
        self._wait_timeout = wait_timeout

        self._click_chain = ActionChains(self._driver).click()
        self._double_click_chain = ActionChains(self._driver).double_click()
        self.__plain_chain = ActionChains(self._driver)

    @property
    def driver(self):
        return self._driver

    @property
    def click_chain(self):
        return self._click_chain

    @property
    def double_click_chain(self):
        return self._double_click_chain

    def find_selenium_element(self, element):
        webdriver_wait = WebDriverWait(self._driver, self._wait_timeout)
        return webdriver_wait.until(EC.presence_of_element_located((By.XPATH, element.xpath)))

    def find_alert(self):
        webdriver_wait = WebDriverWait(self._driver, self._wait_timeout)
        return webdriver_wait.until(EC.alert_is_present())

    def scroll_into_view(self, element):
        self._driver.execute_script("arguments[0].scrollIntoView(true)", element)

    def move_to(self, e, offset_percentages=(0.5, 0.5)):
        rect = e.rect
        x_offset = int(rect['width'] * offset_percentages[0])
        y_offset = int(rect['height'] * offset_percentages[1])
        ActionChains(self._driver).move_to_element_with_offset(e, x_offset, y_offset).perform()

    def wait_and_move_to(self, e):
        self.wait_for_loading()
        e = self.find_selenium_element(e)
        self.scroll_into_view(e)
        self.move_to(e)
        return e

    @staticmethod
    def judge_body_ready(driver):
        return driver.execute_script('return document.readyState == "complete"')

    def wait_for_loading(self):
        webdriver_wait = WebDriverWait(self._driver, self._wait_timeout)
        webdriver_wait.until(SeleniumHelper.judge_body_ready)
        webdriver_wait.until(SeleniumHelper.judge_body_ready)


class BrowserCommander(BaseCommander):

    def __init__(self, driver, wait_timeout=DEFAULT_WAIT_TIMEOUT):
        super().__init__()
        self._driver = driver
        self._selenium_helper = SeleniumHelper(driver, wait_timeout)

    def close(self):
        self._driver.quit()

    @property
    def selenium_helper(self):
        return self._selenium_helper

    def input(self, element, text, send_enter_key=False):
        self.record_msg("input")
        e = self._selenium_helper.wait_and_move_to(element)
        self._selenium_helper.click_chain.perform()
        if send_enter_key:
            e.send_keys(text, Keys.ENTER)
        else:
            e.send_keys(text)

    def click(self, element):
        self.record_msg("click")
        self._selenium_helper.wait_and_move_to(element)
        self._selenium_helper.click_chain.perform()

    def double_click(self, element):
        self._selenium_helper.wait_and_move_to(element)
        self._selenium_helper.double_click_chain.perform()

    def press(self, element, seconds=1):
        pass

    def drag_to(self, source, target, target_position: tuple=(0.5, 0.5)):
        pass

    def navigate(self, url):
        self.record_msg("navigate")
        self._driver.get(url)
        self._selenium_helper.wait_for_loading()

    def switch_to_tab(self, tab_id=None, tab_title=None):
        pass

    def alert_accept(self, input_text=None):
        a = self._selenium_helper.find_alert()
        if not input_text or input_text == '':
            a.send_keys(input_text)
        a.accept()

    def alert_dismiss(self):
        a = self._selenium_helper.find_alert()
        a.dismiss()

    def get_title(self):
        return self._driver.title

    def get_text(self, element):
        e = self._selenium_helper.find_selenium_element(element)
        return e.get_text

    def get_alert_text(self):
        a = self._selenium_helper.find_alert()
        return a.get_text

    def screenshot(self):
        data = self._driver.get_screenshot_as_png()
        self.record_img(data, 'png')


class BrowserCommanderFactory(CommanderFactory):
    def __init__(self, wait_timeout=DEFAULT_WAIT_TIMEOUT):
        self._driver = get_driver()
        self._wait_timeout = wait_timeout

    def _new_commander(self):
        return BrowserCommander(self._driver, self._wait_timeout)
