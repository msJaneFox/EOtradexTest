import pytest
import allure
from PageObject.LoginPage import LoginPage
from PageObject.PaymentPage import PaymentPage
from methods import *


@allure.feature('Auth')
@pytest.mark.parametrize('lang', [[LoginPage.EN_LANG, 'en'],
                                  [LoginPage.CH_LANG, 'zh-Hans'],
                                  [LoginPage.KO_LANG, 'ko'],
                                  [LoginPage.RU_LANG, 'ru'],
                                  [LoginPage.HI_LANG, 'hi-IN']])
def test_change_language(driver, lang):
    """
    Проверяет смену языка интерфейса
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на страницу логина'):
        login_page.get_login_page()

    with allure.step('Выбор языка интерфейса'):
        login_page.select_language(lang[0])

    with allure.step('Проверка языка интерфейса'):
        login_page.check_language(lang[1])


@allure.feature('Auth')
@pytest.mark.parametrize('lang', [LoginPage.EN_LANG,
                                  LoginPage.CH_LANG,
                                  LoginPage.KO_LANG,
                                  LoginPage.RU_LANG,
                                  LoginPage.HI_LANG])
def test_login(driver, lang):
    """
    Проверяет авторизацию
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную и проверка наличия формы логина'):
        login_page.get_login_page()
        login_page.check_login_form()

    with allure.step('Выбор язык интерфейса'):
        login_page.select_language(lang)

    user = get_test_user()
    with allure.step('Ввод данных случайного тестового юзера'):
        login_page.enter_login_data(user)

    payment_page = PaymentPage(driver)
    with allure.step('Проверка появления страницы платежа'):
        payment_page.check_payment_form()


@allure.feature('Auth')
def test_login_with_wrong_email(driver):
    """
    Проверяет напоминание пароля с невалидным email
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    user = [generate_text(), generate_text()]
    with allure.step('Ввод невалидного email в поле напоминания пароля'):
        login_page.enter_login_data(user)

    with allure.step('Проверка наличия формы логина и отсутсвия уведомления о неправильном пароле'):
        login_page.check_login_form()
        assert login_page.check_notification() is False, 'there is no email validation in the email field'


@allure.feature('Auth')
def test_login_non_exist_user(driver):
    """
    Проверяет авторизацию несуществующего юзера
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    user = [generate_text() + '@mail.ru', generate_text()]
    with allure.step('Ввод случайных валидных данных несуществующего юзера'):
        login_page.enter_login_data(user)

    with allure.step('Проверка появления сообщения о неправильном пароле'):
        assert login_page.check_notification() is True, 'Password error message did not appear'

    with allure.step('Нажатие close и проверка закрытия сообщения'):
        login_page.close_message()
        assert login_page.check_notification() is False, 'Password error message not closed'


@allure.feature('Auth')
def test_forgot_password(driver):
    """
    Проверяет напоминание пароля
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    with allure.step('Нажатие на кнопку Забыл пароль'):
        login_page.click_forgot_password()

    email = generate_text() + '@mail.ru'
    with allure.step('Ввод случайного валидного email'):
        login_page.enter_email_in_forgot_field(email)

    with allure.step('Нажатие на кнопку отправки пароля и проверка сообщения об отправке'):
        login_page.click_repair_password()
        assert login_page.check_notification() is True, 'New password message did not appear'

    with allure.step('Нажатие close и проверка закрытия сообщения'):
        login_page.close_message()
        assert login_page.check_notification() is False, 'New password message not closed'


@allure.feature('Auth')
def test_forgot_password_with_wrong_email(driver):
    """
    Проверяет напоминание пароля с невалидным email
    :return:
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    with allure.step('Нажатие на кнопку Забыл пароль'):
        login_page.click_forgot_password()

    email = generate_text()
    with allure.step('Ввод невалидного email'):
        login_page.enter_email_in_forgot_field(email)

    with allure.step('Нажатие на кнопку отправки пароля'):
        login_page.click_repair_password()

    with allure.step('Проверка отсутсвия нотификации об отправке'):
        assert login_page.check_notification() is False, 'there is no email validation in the forgot password field'
