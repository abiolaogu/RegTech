import hashlib
import os
import shutil
from datetime import datetime
import json

class VaultService:
    def __init__(self, base_path="./vault_storage"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        # In a real system, we'd use a tamper-evident DB for this ledger
        self.ledger_path = os.path.join(base_path, "ledger.json")
        self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                self.ledger = json.load(f)
        else:
            self.ledger = []

    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)

    def _calculate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def store_document(self, category: str, file_path: str, meta: dict) -> dict:
        """
        Stores a document immutably.
        category: 'whistleblowing' or 'related-party'
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Source file {file_path} not found")

        # 1. Hashing
        file_hash = self._calculate_hash(file_path)

        # 2. Immutable Path logic
        year = datetime.now().year
        dest_dir = os.path.join(self.base_path, category, str(year))
        os.makedirs(dest_dir, exist_ok=True)
        
        filename = f"{file_hash[:12]}_{os.path.basename(file_path)}"
        dest_path = os.path.join(dest_dir, filename)

        # 3. Write Once (Simulated by checking existence)
        if os.path.exists(dest_path):
            return {"status": "exists", "path": dest_path, "hash": file_hash}
        
        shutil.copy(file_path, dest_path)
        
        # 4. Lock (Simulate by removing write permissions)
        os.chmod(dest_path, 0o444) 

        # 5. Ledger Entry
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category,
            "hash": file_hash,
            "path": dest_path,
            "meta": meta
        }
        self.ledger.append(entry)
        self._save_ledger()

        return {"status": "stored", "path": dest_path, "hash": file_hash}
