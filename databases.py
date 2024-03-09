from sqlite3 import connect, Connection, Cursor
from aiogram.types import Message


class DataBases:
    CONNECTION: Connection = connect("moderation.db")
    CURSOR: Cursor = CONNECTION.cursor()

    def __init__(self):
        self.admins = self.AdminsDB()
        self.blacklist = self.BlackListWords()
        self.messages = self.MessagesDB()

    def __del__(self):
        self.CONNECTION.close()

    class BlackListWords:
        def __init__(self):
            self.create_table()

        @staticmethod
        def create_table():
            DataBases.CURSOR.execute("""CREATE TABLE IF NOT EXISTS BlackListWords (
                word TEXT
            )""")
            DataBases.CONNECTION.commit()

        @staticmethod
        def add_word(word: str):
            DataBases.CURSOR.execute("""INSERT INTO BlackListWords VALUES (?)""",
                                     (word,))
            DataBases.CONNECTION.commit()

        @staticmethod
        def remove_word(word: str):
            DataBases.CURSOR.execute("""DELETE FROM BlackListWords WHERE word = ?""",
                                     (word,))
            DataBases.CONNECTION.commit()

        @staticmethod
        def clear():
            DataBases.CURSOR.execute("""DELETE FROM BlackListWords""")
            DataBases.CONNECTION.commit()

        @staticmethod
        def is_word_in_blacklist(word: str):
            DataBases.CURSOR.execute("""SELECT * FROM BlackListWords WHERE word = ?""",
                                     (word,))
            return bool(DataBases.CURSOR.fetchone())

    class AdminsDB:
        def __init__(self):
            self.create_table()

        @staticmethod
        def create_table():
            DataBases.CURSOR.execute("""CREATE TABLE IF NOT EXISTS Admins (
                telegram_user_id INTEGER
            )""")
            DataBases.CONNECTION.commit()

        @staticmethod
        def add_admin(telegram_user_id: int):
            DataBases.CURSOR.execute("""INSERT INTO Admins VALUES (?)""",
                                     (telegram_user_id,))
            DataBases.CONNECTION.commit()

        @staticmethod
        def remove_admin(telegram_user_id: int):
            DataBases.CURSOR.execute("""DELETE FROM Admins WHERE telegram_user_id = ?""",
                                     (telegram_user_id,))
            DataBases.CONNECTION.commit()

        @staticmethod
        def is_user_admin(telegram_user_id: int) -> bool:
            DataBases.CURSOR.execute("""SELECT * FROM Admins WHERE telegram_user_id = ?""",
                                     (telegram_user_id,))
            return bool(DataBases.CURSOR.fetchone())

    class MessagesDB:
        def __init__(self):
            self.create_table()

        @staticmethod
        def create_table():
            DataBases.CURSOR.execute("""CREATE TABLE IF NOT EXISTS Messages (
                telegram_user_id INTEGER,
                message_text TEXT,
                time INTEGER
            )""")
            DataBases.CONNECTION.commit()

        @staticmethod
        def add_message(message: Message):
            DataBases.CURSOR.execute("""INSERT INTO Messages VALUES (?, ?, ?)""",
                                     (message.from_user.id, message.text, message.date.timestamp()))
            DataBases.CONNECTION.commit()

        @staticmethod
        def get_last_equal_message_data(text: str):
            DataBases.CURSOR.execute("""SELECT * FROM Messages ORDER BY time DESC LIMIT 1""")
            return DataBases.CURSOR.fetchone()


databases = DataBases()
__all__ = ["databases"]
