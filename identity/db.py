import sqlite3


def create_currency_trades_table(db_path):
    """
    Creates the currency_trades table if it doesn't exist.

    :param db_path: String denoting the path of the identity database
    :return: None
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency_trades
        (
            id INTEGER PRIMARY KEY,
            currency_trade_id VARCHAR(10) UNIQUE NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
