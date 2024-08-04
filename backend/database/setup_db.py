import sqlite3
import os

def setup_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'wikipedia.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        from_page_id INTEGER,
        to_page_id INTEGER,
        FOREIGN KEY (from_page_id) REFERENCES pages (id),
        FOREIGN KEY (to_page_id) REFERENCES pages (id)
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pages_title ON pages (title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_links_from ON links (from_page_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_links_to ON links (to_page_id)')

    conn.commit()
    conn.close()

    print("Database setup completed successfully.")

if __name__ == "__main__":
    setup_database()