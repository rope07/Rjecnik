import sqlite3

db_path = 'Databases/spa_dictionary.db'

def spanish_collation(str1, str2):
    spanish_order = " aábcdeéfghiíjklmnñoópqrstuúüvwxyz"
    
    str1 = str1.lower()
    str2 = str2.lower()
    
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            pos1 = spanish_order.find(c1)
            pos2 = spanish_order.find(c2)
            return pos1 - pos2
    
    return len(str1) - len(str2)

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE if not exists dictionary (
                id INTEGER,
                spa_word TEXT NOT NULL,
                word_type TEXT NOT NULL,
                word_gender TEXT,
                cro_word TEXT NOT NULL
                )
            """)
    
    conn.commit()
    conn.close()

def query_db():
    conn = sqlite3.connect(db_path)
    conn.create_collation("SPANISH", spanish_collation)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM dictionary ORDER BY spa_word COLLATE SPANISH")
    
    words = cursor.fetchall()
    conn.commit()
    conn.close()
    return words

def search_words(lookup_record):
    conn = sqlite3.connect(db_path)
    conn.create_collation("SPANISH", spanish_collation)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM dictionary WHERE spa_word like ? ORDER BY spa_word COLLATE SPANISH", (lookup_record,))
    
    words = cursor.fetchall()
    conn.commit()
    conn.close()
    return words

def search_croatian(lookup_record):
    conn = sqlite3.connect(db_path)
    conn.create_collation("SPANISH", spanish_collation)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM dictionary WHERE cro_word like '%' || ? || '%' ORDER BY spa_word COLLATE SPANISH", (lookup_record,))
    
    words = cursor.fetchall()
    conn.commit()
    conn.close()
    return words

def delete_word_from_db(word_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE from dictionary WHERE oid=?", (word_id,))
    conn.commit()
    conn.close()

def delete_all_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE dictionary")
    conn.commit()
    conn.close()

def update_word_in_db(word_id, spa_word, word_type, word_gender, cro_word):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""UPDATE dictionary SET
                   spa_word = ?,
                   word_type = ?,
                   word_gender = ?,
                   cro_word = ?
                   WHERE oid = ?""",
                   (spa_word, word_type, word_gender, cro_word, word_id))
    
    conn.commit()
    conn.close()


def add_word_to_db(word_id, spa_word, word_type, word_gender, cro_word):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dictionary VALUES (?, ?, ?, ?, ?)",
                   (word_id, spa_word, word_type, word_gender, cro_word))
    
    conn.commit()
    conn.close()

def count_words():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) from dictionary")
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return count