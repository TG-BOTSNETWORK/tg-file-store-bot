import psycopg2

DATABASE_URL = "postgres://askmadhi:OHHUSsmc7WUshSsgXGkjqPN5_0PGUX3-@berry.db.elephantsql.com/askmadhi"

def Connect(query, values=None, fetch=False):
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

def add_user(user_id):
    query = "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING;"
    Connect(query, (user_id,))

def add_chat(chat_id):
    query = "INSERT INTO chats (chat_id) VALUES (%s) ON CONFLICT DO NOTHING;"
    Connect(query, (chat_id,))

def get_users():
    query = "SELECT COUNT(user_id) FROM users;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def get_chats():
    query = "SELECT COUNT(chat_id) FROM chats;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0
