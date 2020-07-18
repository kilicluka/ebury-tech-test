# -*- coding: utf-8 -*-

import random
import string
import threading
import sqlite3
import os

from .db import create_currency_trades_table

"""
Directory of the current module
"""
CURRENT_DIR = os.path.dirname(__file__)

"""
String denoting the path of the identity database
"""
DB_PATH = os.path.join(CURRENT_DIR, '../identity.db')

create_currency_trades_table(DB_PATH)

"""
Maximum number of allowed sqlite variables (as per its documentation)
"""
SQLITE_MAX_VARIABLE_NUMBER = 999

lock = threading.Lock()


def generate(number_of_ids_to_generate=1):
    """
    Generates unique currency trade IDs of 7 alphanumeric characters (A-Z, a-z, 0-9).

    :param number_of_ids_to_generate: How many ids to generate
    :return: Single ID or a list of IDs if more than 1 was requested
    """
    db_connection = sqlite3.connect(DB_PATH)
    currency_trade_ids = [
        get_currency_trade_id() for _ in range(number_of_ids_to_generate)
    ]

    with lock:
        store_currency_trade_ids_to_db(currency_trade_ids, db_connection)

    db_connection.close()

    return currency_trade_ids[0] if number_of_ids_to_generate == 1 else currency_trade_ids


def store_currency_trade_ids_to_db(currency_trade_ids, db_connection):
    """
    Stores the currency trade IDs in the database. If any of the IDs are already present in the
    database, new ones are created until they are all unique. The list of the currency trade IDs
    is stored in chunks of SQLITE_MAX_VARIABLE_NUMBER size.

    :param currency_trade_ids: List of the generated currency trade IDs
    :param db_connection: Connection to the underlying database
    :return: None
    """
    db_cursor = db_connection.cursor()

    for i in range(0, len(currency_trade_ids), SQLITE_MAX_VARIABLE_NUMBER):
        ids_chunk = currency_trade_ids[i:i + SQLITE_MAX_VARIABLE_NUMBER]

        while True:
            try:
                db_cursor.execute('''
                    INSERT INTO currency_trades(currency_trade_id) VALUES {}
                '''.format(generate_sql_insert_bindings_for_list(ids_chunk)), ids_chunk)
                db_connection.commit()
            except sqlite3.IntegrityError:
                regenerate_duplicates(ids_chunk, db_connection)
                currency_trade_ids[i:i + SQLITE_MAX_VARIABLE_NUMBER] = ids_chunk
                continue
            break


def get_currency_trade_id():
    """
    Generates a currency trade ID of 7 alphanumeric characters (A-Z, a-z, 0-9).

    :return: String of of 7 alphanumeric characters (A-Z, a-z, 0-9)
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))


def regenerate_duplicates(currency_trade_ids, db_connection):
    """
    Replaces the currency trade IDs already present in the database with the new ones.

    :param currency_trade_ids: List of the generated currency trade IDs
    :param db_connection: Connection to the underlying database
    :return: None
    """
    duplicate_ids = get_duplicates_from_db(currency_trade_ids, db_connection)

    for id_ in duplicate_ids:
        currency_trade_ids.remove(id_)
        new_id = get_currency_trade_id()
        currency_trade_ids.append(new_id)


def get_duplicates_from_db(currency_trade_ids, db_connection):
    """
    Gets the list of the generated currency trade IDs already present in the database (duplicates).
    The list of the generated currency trade IDs is checked in chunks of
    SQLITE_MAX_VARIABLE_NUMBER size.

    :param currency_trade_ids: List of the generated currency trade IDs
    :param db_connection: Connection to the underlying database
    :return: List of the currency trade IDs already present in the database
    """
    db_cursor = db_connection.cursor()
    duplicate_ids = []

    for i in range(0, len(currency_trade_ids), SQLITE_MAX_VARIABLE_NUMBER):
        ids_chunk = currency_trade_ids[i:i + SQLITE_MAX_VARIABLE_NUMBER]

        db_cursor.execute('''
            SELECT currency_trade_id
            FROM currency_trades
            WHERE currency_trade_id IN ({})
        '''.format(generate_sql_in_operator_bindings_for_list(ids_chunk)), ids_chunk)

        duplicate_ids.extend([id_[0] for id_ in db_cursor.fetchall()])

    return duplicate_ids


def generate_sql_insert_bindings_for_list(values):
    """
    Generates the length of the values number of sqlite binding parameters used in a bulk insert
    query.

    :param values: List of values for which to generate the binding parameters
    :return: String of the binding parameters
    """
    return ','.join('(?)' for _ in values)


def generate_sql_in_operator_bindings_for_list(values):
    """
    Generates the length of the values number of sqlite binding parameters used with the IN
    operator.

    :param values: List of values for which to generate the binding parameters
    :return: String of the binding parameters
    """
    return ','.join('?' for _ in values)


def generate_bulk(number_of_ids_to_generate):
    """
    Generates multiple unique currency trade IDs of 7 alphanumeric characters (A-Z, a-z, 0-9).

    :param number_of_ids_to_generate: How many ids to generate
    :return: List of IDs
    """
    return generate(number_of_ids_to_generate)
