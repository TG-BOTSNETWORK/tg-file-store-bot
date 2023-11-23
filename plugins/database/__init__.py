import psycopg2

DATABASE_URL = "postgres://askmadhi:OHHUSsmc7WUshSsgXGkjqPN5_0PGUX3-@berry.db.elephantsql.com/askmadhi"

def connect(query, values=None, fetch=False):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        connection.commit()

        if fetch:
            return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

create_users = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL
);
"""

create_chats = """
CREATE TABLE IF NOT EXISTS chats (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL
);
"""

connect(create_users)
connect(create_chats)

def add_user(user_id):
    query = "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;"
    result = connect(query, (user_id,), fetch=True)
    return result[0][0] if result else None

def add_chat(chat_id):
    query = "INSERT INTO chats (chat_id) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;"
    result = connect(query, (chat_id,), fetch=True)
    return result[0][0] if result else None

def get_users():
    query = "SELECT COUNT(user_id) FROM users;"
    result = connect(query, fetch=True)
    return result[0][0] if result else 0

def get_chats():
    query = "SELECT COUNT(chat_id) FROM chats;"
    result = connect(query, fetch=True)
    return result[0][0] if result else 0
