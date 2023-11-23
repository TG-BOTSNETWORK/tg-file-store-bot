from plugins.database import Connect

create_total_files = """
CREATE TABLE IF NOT EXISTS total_file (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_saved_files = """
CREATE TABLE IF NOT EXISTS saved_file (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_deleted_files = """
CREATE TABLE IF NOT EXISTS deleted_file (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    delete_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

Connect(create_total_files)
Connect(create_saved_files)
Connect(create_deleted_files)

def add_total_files():
    query = "SELECT COUNT(*) FROM uploaded_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def add_saved_files():
    query = "SELECT COUNT(*) FROM saved_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def add_deleted_files():
    query = "SELECT COUNT(*) FROM deleted_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0
