from plugins.database import Connect


create_premium_users = """
CREATE TABLE IF NOT EXISTS premium_users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL
);
"""
Connect(create_premium_users)

def add_premium_user(user_id):
    query = "INSERT INTO premium_users (user_id) VALUES (%s) ON CONFLICT DO NOTHING;"
    Connect(query, (user_id,))

def get_premium_users():
    query = "SELECT user_id FROM premium_users;"
    result = Connect(query, fetch=True)
    return [user_id for user_id, in result] if result else []

def delete_premium_user(user_id):
    query = "DELETE FROM premium_users WHERE user_id = %s;"
    Connect(query, (user_id,))
