from sqlite3 import connect, Connection, Cursor


class TelegramUsersDB:
    def __init__(self):
        self.connection: Connection = connect("tg_users.db")
        self.cursor: Cursor = self.connection.cursor()

        self.__create_table()

    def __create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            id integer,
            languages text
        )""")
        self.connection.commit()

    def is_user_in_db(self, id_):
        self.cursor.execute("""SELECT id FROM Users WHERE id = ?""",
                            (id_,))
        return bool(self.cursor.fetchone())

    def add_user(self, id_, languages):
        if self.is_user_in_db(id_):
            self.cursor.execute("""UPDATE Users SET languages = ? WHERE id = ?""",
                                (id_, languages))
        else:
            self.cursor.execute("""INSERT INTO Users VALUES (?, ?)""",
                                (id_, languages))
        self.connection.commit()

    def remove_user(self, id_):
        self.cursor.execute("""DELETE FROM Users WHERE id = ?""",
                            (id_,))
        self.connection.commit()

    def select_by_lang(self, lang):
        self.cursor.execute("""SELECT id FROM Users WHERE languages LIKE ?""",
                            (f"%{lang}%",))
        ids = []
        for user in self.cursor.fetchall():
            for data in user:
                ids.append(data)

        return ids


tg_db = TelegramUsersDB()
__all__ = ["tg_db"]

if __name__ == '__main__':
    tg_db.add_user(218981, "python")
    tg_db.add_user(22118981, "python javascript")
    tg_db.add_user(218981843, "java")
