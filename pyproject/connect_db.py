import sqlite3

# データベースの初期化
def initialize_database():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    # chatテーブルを作成
    # 3つのカラム
    c.execute('''CREATE TABLE IF NOT EXISTS chat (
        title TEXT,
        my_question TEXT,
        teacher_answer TEXT
    )''')
    conn.commit()
    conn.close()

# 質問と回答の登録
def insert_chat(title, my_question, teacher_answer):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO chat (title, my_question, teacher_answer) VALUES (?, ?, ?)',
              (title, my_question, teacher_answer))
    conn.commit()
    conn.close()

# 質問と回答の取得
def get_all_chats():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT title, my_question, teacher_answer FROM chat')
    chats = c.fetchall()
    conn.close()
    return chats