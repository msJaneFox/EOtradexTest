# -*- coding: utf-8 -*-
import time
from WebBase import WebBase


class WebElement(WebBase):
    """
    Базовые манипуляции с элементами
    """
    MAX_WAIT_TIME = 15

    def __init__(self, elem, driver):
        super().__init__(driver)
        self.elem = elem
        self.driver = driver

    def __getattr__(self, attr):
        prop = getattr(self.elem, attr)
        return prop

    def click(self):
        """
        Кликнуть по элементу

        :return:
        """
        element = self.elem
        assert element, "Елемент не найден, либо невидимый"
        self.move_to_element(self.elem)
        time.sleep(1)
        self.elem.click()
        self.wait_interactive_ready_state()

        return self
