from sqlite3 import connect, Connection, Cursor


class DBS:
    CONNECTION = connect("kufar.db")
    CURSOR = CONNECTION.cursor()

    def __init__(self):
        self.users_db = self.UsersDB()
        self.posts_db = self.PostsDB()

    def __del__(self):
        self.CONNECTION.close()

    class UsersDB:
        def __init__(self):
            self.create_users_table()

        @staticmethod
        def create_users_table():
            DBS.CURSOR.execute("""CREATE TABLE IF NOT EXISTS Users (
                telegram_id INTEGER,
                name TEXT,
                contacts TEXT
            )
            """)
            DBS.CONNECTION.commit()

        @staticmethod
        def add_user(telegram_id: int, name: str, contacts: str):
            DBS.CURSOR.execute("""INSERT INTO Users VALUES (?, ?, ?)""",
                               (telegram_id, name, contacts))
            DBS.CONNECTION.commit()

        @staticmethod
        def get_user_data_by_telegram_id(telegram_id: int) -> tuple:
            DBS.CURSOR.execute("""SELECT * FROM Users WHERE telegram_id = ?""",
                               (telegram_id,))

            return DBS.CURSOR.fetchone()

        @staticmethod
        def remove_user(telegram_id: int):
            DBS.CURSOR.execute("""DELETE FROM Users WHERE telegram_id = ?""",
                               (telegram_id,))
            DBS.CONNECTION.commit()

    class PostsDB:
        def __init__(self):
            self.create_table()

        @staticmethod
        def create_table():
            DBS.CURSOR.execute("""CREATE TABLE IF NOT EXISTS Posts (
                post_unique_id TEXT,
                post_owner_telegram_id INTEGER,
                post_title TEXT,
                post_description TEXT,
                deleted INTEGER,
                kufar_channel_id INTEGER,
                kufar_message_id INTEGER
            )""")
            DBS.CONNECTION.commit()

        @staticmethod
        def add_post(post_unique_id: str, post_owner_telegram_id: int, post_title: str, post_description: str,
                     kufar_channel_id: int, kufar_message_id: int):
            DBS.CURSOR.execute("""INSERT INTO Posts VALUES (?, ?, ?, ?, ?, ?, ?)""",
                               (post_unique_id, post_owner_telegram_id, post_title, post_description, 0,
                                kufar_channel_id, kufar_message_id))
            DBS.CONNECTION.commit()

        @staticmethod
        def get_user_posts(telegram_user_id: int, offset: int, limit: int):
            DBS.CURSOR.execute("""SELECT * FROM Posts WHERE post_owner_telegram_id = ? AND deleted = 0
                                LIMIT ? OFFSET ?""",
                               (telegram_user_id, limit, offset))
            return DBS.CURSOR.fetchall()

        @staticmethod
        def get_post_data_by_post_id(post_unique_id: str):
            DBS.CURSOR.execute("""SELECT * FROM Posts WHERE post_unique_id = ?""",
                               (post_unique_id,))
            return DBS.CURSOR.fetchone()

        @staticmethod
        def update_post_title(post_unique_id: str, title: str):
            DBS.CURSOR.execute("""UPDATE Posts SET post_title = ? WHERE post_unique_id = ?""",
                               (title, post_unique_id))
            DBS.CONNECTION.commit()

        @staticmethod
        def update_post_description(post_unique_id: str, description: str):
            DBS.CURSOR.execute("""UPDATE Posts SET post_description = ? WHERE post_unique_id = ?""",
                               (description, post_unique_id))
            DBS.CONNECTION.commit()

        @staticmethod
        def set_deleted(post_unique_id: str):
            DBS.CURSOR.execute("""UPDATE Posts SET deleted = 1 WHERE post_unique_id = ?""",
                               (post_unique_id,))
            DBS.CONNECTION.commit()


database = DBS()
__all__ = ["database"]
