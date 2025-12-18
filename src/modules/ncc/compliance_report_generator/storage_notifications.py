import os
import shutil
import uuid
import psycopg2
from typing import Optional

# --- LumaDB Configuration ---
DB_URL = os.getenv("DATABASE_URL", "postgresql://lumadb:lumadb@lumadb:5432/default")

# --- Storage Service ---

class StorageService:
    def __init__(self, provider='lumadb', bucket_name='regtech-reports'):
        self.provider = provider
        self.bucket_name = bucket_name
        self.local_storage_path = os.path.join(os.getcwd(), 'storage')
        self._ensure_table()
        
    def _get_connection(self):
        return psycopg2.connect(DB_URL)

    def _ensure_table(self):
        """Creates the document_storage table in LumaDB if it doesn't exist."""
        if self.provider != 'lumadb':
            return
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS document_storage (
                    id TEXT PRIMARY KEY,
                    filename TEXT,
                    content BYTEA,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[Storage] LumaDB init failed: {e}")

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Uploads a file to the configured storage provider.
        Returns the clickable URL or path.
        """
        if self.provider == 'local':
            os.makedirs(self.local_storage_path, exist_ok=True)
            dest_path = os.path.join(self.local_storage_path, destination_name)
            shutil.copy(file_path, dest_path)
            return f"file://{dest_path}"
        
        elif self.provider == 'lumadb':
            # Store file content in LumaDB BLOB column
            doc_id = str(uuid.uuid4())
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()

                conn = self._get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO document_storage (id, filename, content) VALUES (%s, %s, %s)",
                    (doc_id, destination_name, psycopg2.Binary(file_content))
                )
                conn.commit()
                conn.close()
                
                # Retrieve URL (Pseudo-URL for API to serve)
                return f"/api/documents/{doc_id}"
            
            except Exception as e:
                print(f"[Storage] Failed to upload to LumaDB: {e}")
                return ""
        
        return ""

# --- Notification Service ---

class NotificationService:
    def send_email(self, recipient: str, subject: str, body: str):
        """
        Mock email sender. In production, use SMTP or SES.
        """
        print(f"--- EMAIL SENT TO {recipient} ---")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("-------------------------------")

    def send_slack_alert(self, channel: str, message: str):
        """
        Mock Slack sender.
        """
        print(f"--- SLACK ALERT TO {channel} ---")
        print(f"Message: {message}")
        print("--------------------------------")
