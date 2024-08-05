import sqlite3
import os
import tempfile
from google.cloud import storage
import logging

class Database:
    def __init__(self, bucket_name, blob_name):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.local_db_path = os.path.join(tempfile.gettempdir(), 'sdow.sqlite')
        
        logging.info(f"Initializing database. Local path: {self.local_db_path}")
        
        self.download_db_from_gcs()
        
        try:
            self.conn = sqlite3.connect(self.local_db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.arraysize = 1000
            logging.info("Database connection established successfully")
        except sqlite3.DatabaseError as e:
            logging.error(f"Error connecting to database: {str(e)}")
            # If the file is not a valid database, delete it and try to download again
            os.remove(self.local_db_path)
            self.download_db_from_gcs()
            self.conn = sqlite3.connect(self.local_db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.arraysize = 1000

    def download_db_from_gcs(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(self.blob_name)

        logging.info(f"Downloading database to {self.local_db_path}")
        blob.download_to_filename(self.local_db_path)
        logging.info("Database download complete")

    def fetch_page(self, page_title):
        query = 'SELECT id, title, is_redirect FROM pages WHERE title = ? COLLATE NOCASE;'
        try:
            self.cursor.execute(query, (page_title,))
            results = self.cursor.fetchall()
            
            if not results:
                raise ValueError(f'Invalid page title {page_title} provided. Page title does not exist.')
            
            for page_id, title, is_redirect in results:
                if not is_redirect:
                    return (page_id, title, False)
            
            # Handle redirects
            redirect_id = results[0][0]
            query = 'SELECT target_id, title FROM redirects INNER JOIN pages ON pages.id = target_id WHERE source_id = ?;'
            self.cursor.execute(query, (redirect_id,))
            result = self.cursor.fetchone()
            
            if not result:
                raise ValueError(f'Invalid page title {page_title} provided. Page title does not exist.')
            
            return (result[0], result[1], True)
        except sqlite3.Error as e:
            logging.error(f"SQLite error in fetch_page: {str(e)}")
            raise

    def fetch_outgoing_links(self, page_id):
        query = 'SELECT outgoing_links FROM links WHERE id = ?;'
        self.cursor.execute(query, (page_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return [int(link) for link in result[0].split('|')]
        return []

    def fetch_incoming_links(self, page_id):
        query = 'SELECT incoming_links FROM links WHERE id = ?;'
        self.cursor.execute(query, (page_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return [int(link) for link in result[0].split('|')]
        return []