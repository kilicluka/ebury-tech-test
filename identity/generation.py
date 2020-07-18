# -*- coding: utf-8 -*-

import random
import string


CURRENCY_TRADE_IDS = {}


def generate():
    currency_trade_id = get_seven_character_alphanum()

    while CURRENCY_TRADE_IDS.get(currency_trade_id):
        currency_trade_id = get_seven_character_alphanum()

    CURRENCY_TRADE_IDS[currency_trade_id] = True
    return currency_trade_id


def generate_bulk(number_of_ids_to_generate):
    return [generate() for _ in range(number_of_ids_to_generate)]


def get_seven_character_alphanum():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))
