# -*- coding: utf-8 -*-

import random
import string


CURRENCY_TRADES = []


def generate():
    currency_trade_id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

    while currency_trade_id in CURRENCY_TRADES:
        currency_trade_id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

    CURRENCY_TRADES.append(currency_trade_id)
    return currency_trade_id
