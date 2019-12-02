import sqlite3
class SQLite:
    def __init__(self):
        self.db_name = "mydb.db"

    def connect(self):
        conn = sqlite3.connect(self.db_name)  # или :memory: чтобы сохранить в RAM

        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS messages (id integer PRIMARY KEY, chat_id text, message_text text)")
        cur.execute("INSERT INTO messages(chat_id, message_text) VALUES ('1', 'test text')")
        cur.execute("SELECT * FROM messages")
        conn.commit()
        rows = cur.fetchall()

        a = 1

if __name__ == '__main__':
    print("ERROR lol")
    db = SQLite()
    db.connect()