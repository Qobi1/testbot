import sqlite3
connect = sqlite3.connect('sql.db', check_same_thread=False)
cursor = connect.cursor()

try:
    cursor.execute("""CREATE TABLE "User" (
    "user_id"	INTEGER,
    "language"	TEXT,
    "state"	INTEGER,
    PRIMARY KEY("user_id" AUTOINCREMENT)
    );""")
except:
    pass


def get_user(user_id):
    sql = f"select * from User where user_id={user_id}"
    return cursor.execute(sql).fetchone()


def insert_user(user_id):
    sql = f"Insert into USER(user_id, state, language) values({user_id}, 1, 'None')"
    cursor.execute(sql)
    connect.commit()
    return get_user(user_id)


def update_info(user_id, language=None, state=None):
    if language:
        cursor.execute(f"Update User Set language=?, state=? where user_id=?", [language, state, user_id])
    elif state:
        cursor.execute(f"Update User Set state=? where user_id=?", [state, user_id])
    connect.commit()
    return get_user(user_id)
