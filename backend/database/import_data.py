import sqlite3
import os
import csv

def import_data(pages_file, links_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'wikipedia.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Import pages
    with open(pages_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        cursor.executemany('INSERT OR IGNORE INTO pages (id, title) VALUES (?, ?)', csv_reader)

    # Import links
    with open(links_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        cursor.executemany('INSERT OR IGNORE INTO links (from_page_id, to_page_id) VALUES (?, ?)', csv_reader)

    conn.commit()
    conn.close()

    print("Data import completed successfully.")

if __name__ == "__main__":
    pages_file = 'path/to/your/pages.csv'
    links_file = 'path/to/your/links.csv'
    import_data(pages_file, links_file)