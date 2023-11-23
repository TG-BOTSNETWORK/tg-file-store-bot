from plugins.database import Connect

create_uploaded_files_table = """
CREATE TABLE uploaded_files (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_saved_files_table = """
CREATE TABLE saved_files (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_deleted_files_table = """
CREATE TABLE deleted_files (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    delete_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

Connect(create_uploaded_files_table)
Connect(create_saved_files_table)
Connect(create_deleted_files_table)

def get_uploaded_files_count():
    query = "SELECT COUNT(*) FROM uploaded_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def get_saved_files_count():
    query = "SELECT COUNT(*) FROM saved_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def get_deleted_files_count():
    query = "SELECT COUNT(*) FROM deleted_files;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0
