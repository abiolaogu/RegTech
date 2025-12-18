import sys
import time
import os
import shutil
import psycopg2
import json
import logging
from enum import Enum
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
WATCH_DIR = os.getenv("INGEST_DIR", "./staging_area")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "./processed")
DB_URL = os.getenv("DATABASE_URL", "postgresql://lumadb:lumadb@lumadb:5432/default")

class LumaDBHandler(FileSystemEventHandler):
    def __init__(self):
        self._ensure_dirs()
        self._ensure_table()

    def _ensure_dirs(self):
        os.makedirs(WATCH_DIR, exist_ok=True)
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        logging.info(f"Watch directory: {WATCH_DIR}, processed directory: {PROCESSED_DIR}")

    def _get_connection(self):
        return psycopg2.connect(DB_URL)

    def _ensure_table(self):
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging_area (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL,
                    content TEXT,
                    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            conn.close()
            logging.info("'staging_area' table ready.")
        except Exception as e:
            logging.error(f"DB Init Error: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = event.src_path
        filename = os.path.basename(filepath)
        
        # Simple debounce or check if file is ready (optional)
        logging.info(f"New file detected: {filename}")
        
        try:
            # Read content
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Validate content (basic JSON check)
            if content.lstrip().startswith('{'):
                try:
                    json.loads(content)
                except json.JSONDecodeError as je:
                    raise ValueError(f"Invalid JSON content: {je}")
            
            # Insert to LumaDB
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO staging_area (filename, content) VALUES (%s, %s)",
                (filename, content)
            )
            conn.commit()
            conn.close()
            logging.info(f"Saved {filename} to LumaDB.")
            
            # Move to processed
            dest_path = os.path.join(PROCESSED_DIR, filename)
            shutil.move(filepath, dest_path)
            logging.info(f"Moved {filename} to processed.")
            
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    event_handler = LumaDBHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    
    logging.info(f"--- Starting File Watcher on {WATCH_DIR} ---")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
