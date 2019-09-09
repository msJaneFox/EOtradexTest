from WebElement import WebBase


class PaymentPage(WebBase):
    """
    Методы для работы с элементами страницы платежа
    """
    # Элементы на странице
    RIOT_FORM = '//*[@id="riot-app"]'
    VIP_STATUS = '//*[@name="vip"]/div'
    GOLD_STATUS = '//*[@name="gold"]/div'
    SILVER_STATUS = '//*[@name="silver"]/div'
    MINI_STATUS = '//*[@name="mini"]/div'
    STATUS = '//status-item'
    CURRENCY = '//*[@class="currency"]'
    RUB = '//*[@class="currency"]//*[@name="menu"]//li[1]'
    USD = '//*[@class="currency"]//*[@name="menu"]//li[2]'
    CNH = '//*[@class="currency"]//*[@name="menu"]//li[3]'
    AMOUNT_STATUS = '//span[@class="amount"]'
    AMOUNT_FIELD = '//*[@name="amount"]'
    SUBMIT = '//submit/div'
    BACK = '//*[@class="back"]'
    YOU_GET_SUM = '//*[@class="you-get"]/*[@class="value"]'
    BONUS_ACTIVATOR = '//*[@for="bonus-activator"]'
    SYSTEM_SELECT = '//*[@class="payment-system-selector"]//*[@name="selectfield"]'
    PAYMENT_SYSTEMS = '//*[@class="payment-system-selector"]//li[{}]'
    PAYMENT_SYSTEMS_NAME = '//*[@class="payment-system-selector"]//li[{}]/*[@class="title"]'
    PHONE_FIELD = '//*[@name="phone"]'
    PHONE_SUBMIT = '//phone//submit/div/a'

    def __init__(self, driver, timeout=10):
        super(PaymentPage, self).__init__(driver)
        self.url = 'https://qa:Af4shrewyirlyuds@ibitcy.com/interview/qa/mobile-deposit/#/payment'
        driver.implicitly_wait(timeout)

    def check_payment_form(self):
        """
        Проверяет наличие формы платежа
        :return:
        """
        form = self.find_element_by_xpath(self.RIOT_FORM).get_attribute('data-is')
        assert form == 'payment', 'Error in payment page after login'

    def check_processed_form(self):
        """
        Проверяет наличие формы совершенного платежа
        :return:
        """
        form = self.find_element_by_xpath(self.RIOT_FORM).get_attribute('data-is')
        assert form == 'process-payment', 'Error in process-payment page after payment'

    def click_status(self, status):
        """
        Нажимает на статус
        :return:
        """
        status_bth = self.find_element_by_xpath(status)
        status_bth.click()

    def click_currency(self):
        """
        Нажимает на валюту
        :return:
        """
        currency = self.find_element_by_xpath(self.CURRENCY)
        currency.click()

    def click_silver_status(self):
        """
        Нажимает на silver статус
        :return:
        """
        silver = self.find_element_by_xpath(self.SILVER_STATUS)
        silver.click()

    def select_currency(self, currency):
        """
        Выбирает валюту
        :return:
        """
        currency_select = self.find_element_by_xpath(currency)
        currency_select.click()

    def enter_amount(self, amount):
        """
        Выбирает валюту
        :return:
        """
        amount_field = self.find_element_by_xpath(self.AMOUNT_FIELD)
        amount_field.clear()
        amount_field.send_keys(amount)

    def get_active_status(self):
        """
        Возвращает активный статус
        :return:
        """
        status_active = self.find_element_by_xpath(self.STATUS).get_attribute('active')
        return status_active

    def get_amount_status(self, status):
        """
        Возвращает минимульную сумму статуса
        :return:
        """
        amount_status = self.find_element_by_xpath(status+self.AMOUNT_STATUS).text
        return int(amount_status[1:])

    def click_submit(self):
        """
        Нажимает submit
        :return:
        """
        submit = self.find_element_by_xpath(self.SUBMIT)
        submit.click()

    def click_back(self):
        """
        Нажимает back
        :return:
        """
        back = self.find_element_by_xpath(self.BACK)
        back.click()

    def get_sum_you_get(self):
        """
        Возвращает сумму из поля you get
        :return:
        """
        amount = self.find_element_by_xpath(self.YOU_GET_SUM).text
        return int(amount[1:])

    def click_bonus_activator(self):
        """
        Нажимает на чекбокс бонуса
        :return:
        """
        self.driver.execute_script('document.getElementById("{}").click();'.format(self.BONUS_ACTIVATOR))

    def click_payment_system(self):
        """
        Нажимает на выбор системы оплаты
        :return:
        """
        system = self.find_element_by_xpath(self.SYSTEM_SELECT)
        system.click()

    def select_payment_system(self, index):
        """
        Выбирает систему оплаты
        :return:
        """
        system = self.find_element_by_xpath(self.PAYMENT_SYSTEMS.format(index))
        system_name = self.find_element_by_xpath(self.PAYMENT_SYSTEMS_NAME.format(index)).text
        system.click()
        return system_name

    def enter_phone(self, phone):
        """
        Вводит номер телефона для QIWI
        :return:
        """
        phone_field = self.find_element_by_xpath(self.PHONE_FIELD)
        phone_field.send_keys(phone)
        phone_submit = self.find_element_by_xpath(self.PHONE_SUBMIT)
        phone_submit.click()

