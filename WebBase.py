# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException,\
    NoSuchWindowException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class WebBase(object):
    MAX_WAIT_TIME = 15
    TIMEOUT_STEP = 0.5

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def __custom_find_by(self, selenium_method, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        Кастомная обертка вокруг всех методов find_element_by_ для поддержки таймаутов и поиска невидимых элементов

        :param str selenium_method:
        :param str val:
        :param int timeout:
        :param bool wait_element_visibility:
        :return:
        """
        from WebElement import WebElement
        driver = self.driver if not isinstance(self, WebElement) else self.elem

        if not isinstance(self, WebElement):
            self.wait_interactive_ready_state()

        def expected_condition(d):
            prop = getattr(d, selenium_method)
            # получаем список элементов
            time.sleep(self.TIMEOUT_STEP)
            elems = prop(val)
            # если элементов не нашлось вообще, то падаем и пробуем опять
            if not elems:
                raise NoSuchElementException
            for el in elems:
                # если элемент уже имеется и видимый, то сразу же вернем его и выйдем
                if el.is_displayed():
                    return el
                # если видимость и не нужна, то сразу же возвращаем этот элемент
                if not wait_element_visibility:
                    return el
                # если элемент это поле для выбора файла, то вернем даже если оно скрыто
                type_attribute = el.get_attribute('type')
                if type_attribute and str(type_attribute).lower().strip() == "file":
                    return el
            # найти ничего не удалось. Падаем и пробуем опять.
            raise NoSuchElementException

        wait = WebDriverWait(driver, timeout, self.TIMEOUT_STEP)
        return WebElement(wait.until(expected_condition), self.driver)

    def __custom_finds_by(self, selenium_method, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        Кастомная обертка вокруг всех методов find_elements_by_ для поддержки таймаутов и поиска невидимых элементов

        :param str selenium_method:
        :param str val:
        :param int timeout:
        :param bool wait_element_visibility:
        :return:
        """
        from WebElement import WebElement
        driver = self.driver if not isinstance(self, WebElement) else self.elem
        if not isinstance(self, WebElement):
            self.wait_interactive_ready_state()

        def expected_condition(d):
            result = []
            prop = getattr(d, selenium_method)
            time.sleep(self.TIMEOUT_STEP)
            elems = prop(val)
            # если элементов не нашлось вообще, то падаем и пробуем опять
            if not elems:
                raise NoSuchElementException
            for el in elems:
                # если элемент уже имеется и он видимый, то берем его и идем к следующему элементу
                if el.is_displayed():
                    result.append(el)
                    continue
                # если видимость и не нужна, то берем элемент и идем к следующему элементу
                if not wait_element_visibility:
                    result.append(el)
                    continue
                # если элемент это поле для выбора файла, то берем его даже если оно скрыто
                type_attribute = el.get_attribute('type')
                if type_attribute and str(type_attribute).lower().strip() == "file":
                    result.append(el)
            # если найти ничего не удалось, то падаем и пробуем опять
            if not result:
                raise NoSuchElementException
            return result

        wait = WebDriverWait(driver, timeout, self.TIMEOUT_STEP)
        try:
            ret = []
            elements = wait.until(expected_condition)
            for element in elements:
                ret.append(WebElement(element, self.driver))
            return ret
        except Exception:
            return []

    def wait_for_element_visibility(self, selector, timeout=10):

        WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def wait_interactive_ready_state(self):
        """
        Ждет, пока document.readyState превратится в interactive
        :return:
        """
        def interactive_rs(d):
            time.sleep(self.TIMEOUT_STEP)
            ready_state = d.execute_script("return document.readyState")
            if "interactive" in ready_state or "complete" in ready_state:
                return True
            return False
        try:
            WebDriverWait(self.driver, self.MAX_WAIT_TIME * 2).until(
                interactive_rs, message="Страница не загрузилась за {0} c".format(self.MAX_WAIT_TIME*2)
            )
        except (NoSuchWindowException, UnexpectedAlertPresentException, WebDriverException, TypeError):
            return

    def find_element_by_xpath(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_xpath', val, timeout, wait_element_visibility)

    def find_elements_by_xpath(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_xpath', val, timeout, wait_element_visibility)

    def move_to_element(self, element=None):
        """
        Навести курсор на указанный элемент. Если элемент не указан, то попытается навести на тот элемент у которого
        был вызван данный метод
        :type element: WebElement.WebElement
        :return: WebElement.WebElement
        """
        if not element:
            if not self.elem:
                raise Exception("Не передан элемент для наведения курсора")
            element = self
        actions = ActionChains(self.driver).move_to_element(element)
        actions.perform()
        return element
