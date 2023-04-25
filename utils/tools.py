import random
from string import ascii_lowercase, ascii_uppercase


def key(length: int = 15):
    letters = ascii_lowercase + ascii_uppercase
    numbers = ''.join(map(str, range(10)))
    symbols = letters + numbers
    return ''.join([random.choice(symbols) for _ in range(length)])


def get_absolute_value(execute_result):
    if execute_result:
        if execute_result[0]:
            return execute_result[0]
    return False
