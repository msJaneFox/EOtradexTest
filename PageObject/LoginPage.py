import urllib.parse as urlparse
from WebElement import WebBase


class LoginPage(WebBase):
    """
    Методы для работы с элементами страницы логина
    """
    # Элементы на странице
    RIOT_FORM = '//*[@id="riot-app"]'
    EN_LANG = '//*[@class="lang en"]'
    CH_LANG = '//*[@class="lang zh"]'
    KO_LANG = '//*[@class="lang ko"]'
    RU_LANG = '//*[@class="lang ru"]'
    HI_LANG = '//*[@class="lang hi"]'
    EMAIL = '//*[@name="username"]'
    PASSWORD = '//*[@name="password"]'
    SUBMIT = '//login-form/form/*[@class="submit gold"]'
    MESSAGE = '//*[@class="notification"]/*[@class="text"]'
    CLOSE_MESSAGE = '//*[@class="notification"]/*[@class="close"]'
    FORGOT_PASSWORD = '//*[@class="forgot"]'
    FORGOT_FIELD = '//*[@name="forgotPass"]'
    REPAIR_PASSWORD = '//forgot-password/form/*[@class="submit gold"]'

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        self.url = 'https://qa:Af4shrewyirlyuds@ibitcy.com/interview/qa/mobile-deposit/'

    def get_login_page(self):
        """
        Переходит на страницу логина
        :return:
        """
        self.driver.get(self.url)

    def check_login_form(self):
        """
        Проверяет наличие формы логина
        :return:
        """
        form = self.find_element_by_xpath(self.RIOT_FORM).get_attribute('data-is')
        assert form == 'login', 'Error in payment page after login'

    def select_language(self, lang=EN_LANG):
        """
        Выбирает язык интерфейса
        :return:
        """
        language = self.find_element_by_xpath(lang)
        language.click()

    def check_language(self, lang):
        """
        Возвращает язык интерфейса
        :return:
        """
        url = self.driver.current_url
        parsed = urlparse.urlparse(url)
        assert urlparse.parse_qs(parsed.query)['lang'][0] == lang, 'Wrong language in url'

    def enter_login_data(self, user):
        """
        Вводит данные юзера в форму логина
        :return:
        """
        email = self.find_element_by_xpath(self.EMAIL)
        email.send_keys(user[0])
        password = self.find_element_by_xpath(self.PASSWORD)
        password.send_keys(user[1])
        submit = self.find_element_by_xpath(self.SUBMIT)
        submit.click()

    def check_notification(self):
        """
        Проверяет уведомление
        :return:
        """
        try:
            self.find_element_by_xpath(self.MESSAGE)
            return True
        except Exception as e:
            return False

    def close_message(self):
        """
        Закртывает сообщение о неверном пароле
        :return:
        """
        close = self.find_element_by_xpath(self.CLOSE_MESSAGE)
        close.click()

    def click_forgot_password(self):
        """
        Нажимает на кнопку напоминания пароля
        :return:
        """
        forgot = self.find_element_by_xpath(self.FORGOT_PASSWORD)
        forgot.click()

    def enter_email_in_forgot_field(self, email):
        """
        Вводит email в поле напоминания пароля
        :return:
        """
        forgot = self.find_element_by_xpath(self.FORGOT_FIELD)
        forgot.send_keys(email)

    def click_repair_password(self):
        """
        Нажимает на кнопку отправки пароля
        :return:
        """
        repair = self.find_element_by_xpath(self.REPAIR_PASSWORD)
        repair.click()








