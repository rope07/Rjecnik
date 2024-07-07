import sqlite3

db_path = 'Dictionary/Databases/cze_dictionary.db'

def czech_collation(str1, str2):
    czech_order = " aábcčdďeéěfghchiíjklmnňoópqrřsštťuúůvwxyýzž"
    
    # Normalize input strings to lower case
    str1 = str1.lower()
    str2 = str2.lower()
    
    str1 = str1.replace('ch', 'hžžžž')
    str2 = str2.replace('ch', 'hžžžž')
    
    # Compare the strings character by character based on Czech alphabet order
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            pos1 = czech_order.find(c1)
            pos2 = czech_order.find(c2)
            return pos1 - pos2
    
    # If one string is a prefix of the other, the shorter string is considered smaller
    return len(str1) - len(str2)

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE if not exists dictionary (
                id INTEGER,
                cze_word TEXT NOT NULL,
                word_type TEXT NOT NULL,
                word_gender TEXT,
                cro_word TEXT NOT NULL
                )
            """)
    
    conn.commit()
    conn.close()

def query_db():
    conn = sqlite3.connect(db_path)
    conn.create_collation("CZECH", czech_collation)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM dictionary ORDER BY cze_word COLLATE CZECH")
    
    words = cursor.fetchall()
    conn.commit()
    conn.close()
    return words

def search_words(lookup_record):
    conn = sqlite3.connect(db_path)
    conn.create_collation("CZECH", czech_collation)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM dictionary WHERE cze_word like ? ORDER BY cze_word COLLATE CZECH", (lookup_record,))
    
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

def update_word_in_db(word_id, cze_word, word_type, word_gender, cro_word):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""UPDATE dictionary SET
                   cze_word = ?,
                   word_type = ?,
                   word_gender = ?,
                   cro_word = ?
                   WHERE oid = ?""",
                   (cze_word, word_type, word_gender, cro_word, word_id))
    
    conn.commit()
    conn.close()


def add_word_to_db(word_id, cze_word, word_type, word_gender, cro_word):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dictionary VALUES (?, ?, ?, ?, ?)",
                   (word_id, cze_word, word_type, word_gender, cro_word))
    
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