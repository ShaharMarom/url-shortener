import sqlite3
import os

class URLManger:
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    def __init__(self):
        self.__db_path = "urls.db"
        if not os.path.exists(self.__db_path):
            self.__init_db()

        last_url = self.__get_last_url()
        self.__sequencer = self.__base58_decode(last_url[0]) if last_url is not None else 0


    def __init_db(self):
        with sqlite3.connect(self.__db_path) as con:
            cursor = con.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS urls(
                    ID TEXT PRIMARY KEY,
                    url TEXT
                )
            ''')

    def __get_last_url(self):
        with sqlite3.connect(self.__db_path) as con:
            cursor = con.cursor()
            cursor.execute('''
                SELECT * FROM urls ORDER BY ID DESC LIMIT 1
            ''')
            return cursor.fetchone()

    def __base58_encode(self, num: int) -> str:
        if num == 0:
            return URLManger.BASE58_ALPHABET[0]
        encoded = []
        base = len(URLManger.BASE58_ALPHABET)
        while num:
            num, rem = divmod(num, base)
            encoded.append(URLManger.BASE58_ALPHABET[rem])
        return ''.join(reversed(encoded))

    def __base58_decode(self, encoded_str: str) -> int:
        """Decodes a Base58-encoded string into an integer."""
        base = len(URLManger.BASE58_ALPHABET)
        decoded_num = 0
        for char in encoded_str:
            decoded_num = decoded_num * base + URLManger.BASE58_ALPHABET.index(char)
        return decoded_num

    def get_url(self, url: str):
        with sqlite3.connect(self.__db_path) as con:
            cursor = con.cursor()
            cursor.execute('''
                SELECT * FROM urls WHERE ID = ?
            ''', (url,))
            res = cursor.fetchone()
            return res[1] if res is not None else None

    def __get_url_by_long(self, url: str):
        with sqlite3.connect(self.__db_path) as con:
            cursor = con.cursor()
            cursor.execute('''
                SELECT * FROM urls WHERE url = ?
            ''', (url,))
            return cursor.fetchone()

    def generate_short_url(self, url: str):
        result_url = self.__get_url_by_long(url)
        if result_url is not None:
            return result_url[0]

        result_url = self.__base58_encode(self.__sequencer)
        result_url = ++self.__sequencer

        with sqlite3.connect(self.__db_path) as con:
            cursor = con.cursor()
            cursor.execute('''
                INSERT INTO urls (ID, url)
                        VALUES (?, ?)
            ''', (result_url, url))

        return result_url