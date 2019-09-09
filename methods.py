import random
from random import choice
from string import ascii_uppercase


users = [['username1@name.ru', 'pass1'],
         ['username2@name.ru', 'pass2'],
         ['username3@name.ru', 'pass3'],
         ['username4@name.ru', 'pass4']]


def generate_text(size=12):
    """
    Генерирует случайную строку с заданным размером
    :param size: Длина строки. По умолчанию 12
    :return:
    """
    return (''.join(choice(ascii_uppercase) for i in range(size)))


def get_test_user():
    """
    Возвращает случайного тестового юзера
    """
    return users[random.randint(0, 3)]
