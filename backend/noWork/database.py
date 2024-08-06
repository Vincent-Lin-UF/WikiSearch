import sqlite3
import os
import tempfile
from google.cloud import storage
import logging
import gzip
import shutil

class Database:
    def __init__(self, bucket_name, blob_name):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.local_gz_path = os.path.join(project_dir, 'sdow.sqlite.gz')
        self.local_db_path = os.path.join(project_dir, 'sdow.sqlite')
        
        logging.info(f"Initializing database. Local path: {self.local_db_path}")
        
        self.download_and_decompress_db_from_gcs()
        
        try:
            self.conn = sqlite3.connect(self.local_db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.arraysize = 1000
            logging.info("Database connection established successfully")
        except sqlite3.DatabaseError as e:
            logging.error(f"Error connecting to database: {str(e)}")
            raise

    def download_and_decompress_db_from_gcs(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(self.blob_name)

        logging.info(f"Downloading compressed database to {self.local_gz_path}")
        blob.download_to_filename(self.local_gz_path)
        logging.info("Database download complete")

        logging.info(f"Decompressing database to {self.local_db_path}")
        with gzip.open(self.local_gz_path, 'rb') as f_in:
            with open(self.local_db_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info("Database decompression complete")

        os.remove(self.local_gz_path)

    def fetch_page(self, page_title):
        query = 'SELECT id, title, is_redirect FROM pages WHERE title = ? COLLATE NOCASE;'
        self.cursor.execute(query, (page_title,))
        results = self.cursor.fetchall()
        
        if not results:
            logging.error(f"Page not found: {page_title}")
            raise ValueError(f'Invalid page title {page_title} provided. Page title does not exist.')
        
        for page_id, title, is_redirect in results:
            if not is_redirect:
                logging.info(f"Found page: {title} (ID: {page_id})")
                return (page_id, title, False)
        
        redirect_id = results[0][0]
        query = 'SELECT target_id, title FROM redirects INNER JOIN pages ON pages.id = target_id WHERE source_id = ?;'
        self.cursor.execute(query, (redirect_id,))
        result = self.cursor.fetchone()
        
        if not result:
            logging.error(f"Redirect target not found for: {page_title}")
            raise ValueError(f'Invalid page title {page_title} provided. Page title does not exist.')
        
        logging.info(f"Found redirected page: {result[1]} (ID: {result[0]})")
        return (result[0], result[1], True)

    def fetch_outgoing_links(self, page_id):
        query = 'SELECT outgoing_links FROM links WHERE id = ?;'
        self.cursor.execute(query, (page_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            links = [int(link) for link in result[0].split('|')]
            logging.info(f"Fetched outgoing links for page {page_id}: {links}")
            return links
        logging.info(f"No outgoing links found for page {page_id}")
        return []

    def autocomplete(self, query):
        query = f"{query}%"
        self.cursor.execute('SELECT title FROM pages WHERE title LIKE ? LIMIT 10', (query,))
        results = self.cursor.fetchall()
        return [result[0] for result in results]

    def get_status(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        
        status = {}
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            status[table_name] = count
        
        return status