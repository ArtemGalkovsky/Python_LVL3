from sqlite3 import connect, Connection, Cursor
from os import listdir, getcwd
from json import dumps


class DB:
    def __init__(self) -> None:
        TABLE_NAME = "bot_db.db"

        if TABLE_NAME not in listdir(getcwd()):
            with open(TABLE_NAME, "w+", encoding="UTF-8") as fl:
                print(f"[{__name__}](DB)(__init__) creatiing new DB!")
                fl.write("")

        self.connection: Connection = connect(TABLE_NAME, check_same_thread=False)
        self.cursor: Cursor = self.connection.cursor()
        self.table_name: str = TABLE_NAME

    def __del__(self):
        self.connection.close()

    def create_chat_table(self, chat_id: int):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS 'chat-{chat_id}' (
        id INTEGER PRIMARY KEY,
        current_post TEXT,
        dishes TEXT
        );
        """)
        self.connection.commit()

    def add_categories_message(self, chat_id: int, message_id: int, current_dish_id: str, all_dishes: list[str]) \
            -> None:
        self.create_chat_table(chat_id)
        self.cursor.execute(f"""
        INSERT INTO 'chat-{chat_id}' VALUES (?, ?, ?)
        """, (message_id, current_dish_id, dumps(all_dishes)))
        self.connection.commit()

    def select_categories_message(self, chat_id: int, message_id: int) -> list[tuple[int, str, str],...]:
        self.cursor.execute(f"""
        SELECT current_post, dishes FROM 'chat-{chat_id}' WHERE id = ?
        """, (message_id,))

        return self.cursor.fetchone()

    def update_categories_message_data(self, chat_id: int,  message_id: int, current_dish_id: str) -> None:
        self.cursor.execute(f"""
        UPDATE 'chat-{chat_id}' SET current_post = ? WHERE id = ?""", (current_dish_id, message_id))
        self.connection.commit()
