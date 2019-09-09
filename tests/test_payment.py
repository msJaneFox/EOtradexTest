import pytest
import allure
from PageObject.LoginPage import LoginPage
from PageObject.PaymentPage import PaymentPage
from methods import *


@allure.feature('Payment')
@pytest.mark.parametrize('currency', [PaymentPage.USD,
                                      PaymentPage.RUB,
                                      PaymentPage.CNH])
@pytest.mark.parametrize('status', [PaymentPage.VIP_STATUS,
                                    PaymentPage.GOLD_STATUS,
                                    PaymentPage.SILVER_STATUS,
                                    PaymentPage.MINI_STATUS])
def test_payment_with_change_status_and_currency(driver, currency, status):
    """
    Проверяет оплату со сменой валюты и статуса
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную и проверка наличия формы логина'):
        login_page.get_login_page()
        login_page.check_login_form()

    user = get_test_user()
    with allure.step('Ввод данных случайного тестового юзера'):
        login_page.enter_login_data(user)

    payment_page = PaymentPage(driver)
    with allure.step('Выбор статуса'):
        payment_page.click_status(status)

    with allure.step('Выбор валюты'):
        payment_page.click_currency()
        payment_page.select_currency(currency)

    with allure.step('Нажатие на кнопку оплаты'):
        payment_page.click_submit()

    with allure.step('Проверка наличия формы совершенного платежа'):
        payment_page.check_processed_form()

    with allure.step('Нажатие на back и проверка наличия формы платежа'):
        payment_page.click_back()
        payment_page.check_payment_form()


@pytest.mark.parametrize('status', [[PaymentPage.VIP_STATUS, 'vip'],
                                    [PaymentPage.GOLD_STATUS, 'gold'],
                                    [PaymentPage.SILVER_STATUS, 'silver'],
                                    [PaymentPage.MINI_STATUS, 'mini']])
def test_payment_with_change_amount_and_status(driver, status):
    """
    Проверяет смену статуса при вводе минимальной суммы
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную и проверка наличия формы логина'):
        login_page.get_login_page()
        login_page.check_login_form()

    user = get_test_user()
    with allure.step('Ввод данных случайного тестового юзера'):
        login_page.enter_login_data(user)

    payment_page = PaymentPage(driver)
    with allure.step('Получение минимальной суммы статуса'):
        sum_status = payment_page.get_amount_status(status[0])

    with allure.step('Ввод суммы'):
        payment_page.enter_amount(sum_status)

    with allure.step('Проверка активного статуса'):
        assert payment_page.get_active_status() == status[1]


@allure.feature('Payment')
def test_payment_without_bonus(driver):
    """
    Проверяет оплату без бонуса
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    user = get_test_user()
    with allure.step('Ввод данных случайного тестового юзера'):
        login_page.enter_login_data(user)

    payment_page = PaymentPage(driver)
    with allure.step('Проверка суммы получения с бонусом'):
        sum_status = payment_page.get_amount_status(PaymentPage.GOLD_STATUS)
        sum_get = payment_page.get_sum_you_get()
        assert sum_status*2 == sum_get, 'Wrong amount you get with bonus'

    with allure.step('Выключение бонуса'):
        payment_page.click_bonus_activator()

    with allure.step('Проверка суммы получения без бонуса'):
        sum_status = payment_page.get_amount_status(PaymentPage.GOLD_STATUS)
        sum_get = payment_page.get_sum_you_get()
        assert sum_status == sum_get, 'Wrong amount you get with bonus'

    with allure.step('Нажатие на кнопку оплаты'):
        payment_page.click_submit()

    with allure.step('Проверка наличия формы совершенного платежа'):
        payment_page.check_processed_form()

    with allure.step('Нажатие на back и проверка наличия формы платежа'):
        payment_page.click_back()
        payment_page.check_payment_form()


@allure.feature('Payment')
@pytest.mark.parametrize('index', range(1, 15))
def test_payment_with_change_system(driver, index):
    """
    Проверяет оплату со сменой платежной системы
    """
    login_page = LoginPage(driver)
    with allure.step('Переход на главную'):
        login_page.get_login_page()

    user = get_test_user()
    with allure.step('Ввод данных случайного тестового юзера'):
        login_page.enter_login_data(user)

    payment_page = PaymentPage(driver)
    with allure.step('Нажатие на кнопку выбора системы оплаты'):
        payment_page.click_payment_system()

    with allure.step('Выбор системы оплаты'):
        system_name = payment_page.select_payment_system(index)

    with allure.step('Нажатие на кнопку оплаты'):
        payment_page.click_submit()

    if system_name == 'QIWI':
        with allure.step('Ввод телефона для QIWI'):
            phone = '+'+str(random.randint(79000000000, 79999999999))
            payment_page.enter_phone(phone)

    with allure.step('Проверка наличия формы совершенного платежа'):
        payment_page.check_processed_form()

    with allure.step('Нажатие на back и проверка наличия формы платежа'):
        payment_page.click_back()
        payment_page.check_payment_form()
