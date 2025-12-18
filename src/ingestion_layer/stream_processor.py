from typing import Dict, Any
import asyncio
import json
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

# --- LumaDB Configuration ---
DB_URL = os.getenv("DATABASE_URL", "postgresql://lumadb:lumadb@lumadb:5432/default")

class LumaDBStream:
    def __init__(self):
        self.handlers = {}
        self._ensure_table()

    def _get_connection(self):
        return psycopg2.connect(DB_URL)

    def _ensure_table(self):
        """Creates the system_events table in LumaDB if it doesn't exist."""
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id SERIAL PRIMARY KEY,
                    topic TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            conn.close()
            print("[LumaDB] 'system_events' table ready.")
        except Exception as e:
            print(f"[LumaDB] Connection error (ensure LumaDB is up): {e}")

    def subscriber(self, topic: str):
        def decorator(func):
            self.handlers[topic] = func
            return func
        return decorator

    async def emit(self, topic: str, msg: Dict[str, Any]):
        """Inserts an event into the LumaDB system_events table."""
        print(f"[STREAM] Emitting to '{topic}': {msg}")
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO system_events (topic, payload) VALUES (%s, %s)",
                (topic, json.dumps(msg))
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[STREAM] Emit failed: {e}")

    async def consume_loop(self):
        """Polls LumaDB for unprocessed events and runs handlers."""
        print("[STREAM] Starting LumaDB Consumer Loop...")
        while True:
            try:
                conn = self._get_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)
                
                # Fetch unprocessed events
                cur.execute(
                    "SELECT id, topic, payload FROM system_events WHERE processed = FALSE ORDER BY id ASC LIMIT 10"
                )
                events = cur.fetchall()

                for event in events:
                    topic = event['topic']
                    payload = event['payload']
                    if topic in self.handlers:
                        # Process logic
                        await self.handlers[topic](payload)
                        
                        # Mark as processed
                        cur.execute("UPDATE system_events SET processed = TRUE WHERE id = %s", (event['id'],))
                        conn.commit()
                
                conn.close()
            except Exception as e:
                print(f"[STREAM] Consumer Loop Error: {e}")
            
            await asyncio.sleep(2) # Poll every 2 seconds

broker = LumaDBStream()

# --- Telecom Connector (CDR Parsing) ---
@broker.subscriber("telecom.cdr")
async def handle_cdr(msg: Dict[str, Any]):
    call_duration = msg.get("duration", 0)
    drop_reason = msg.get("termination_code")
    
    if drop_reason == "RADIO_LINK_FAILURE":
        print(f"  -> ALERT: Dropped Call detected! Duration: {call_duration}s")

# --- Banking Connector (ISO 8583 Stream) ---
@broker.subscriber("banking.tx")
async def handle_banking_tx(msg: Dict[str, Any]):
    amount = msg.get("amount", 0)
    if amount > 5_000_000:
        print(f"  -> AML FLAG: High Value Transaction Detected: N{amount}")

# --- Simulation Runner ---
async def run_stream_simulation():
    print("--- Starting LumaDB Stream Simulation ---")
    
    # Start consumer in background
    consumer_task = asyncio.create_task(broker.consume_loop())

    # 1. Telecom Event
    await broker.emit("telecom.cdr", {
        "id": "call_001", 
        "duration": 45, 
        "termination_code": "NORMAL"
    })
    
    await broker.emit("telecom.cdr", {
        "id": "call_002", 
        "duration": 12, 
        "termination_code": "RADIO_LINK_FAILURE"
    })
    
    # 2. Banking Event
    await broker.emit("banking.tx", {
        "tx_id": "tx_999", 
        "amount": 12_500_000, 
        "currency": "NGN"
    })

    # Let consumer catch up
    await asyncio.sleep(5)
    # Note: In real app, consumer runs forever. Here we exit.
    consumer_task.cancel()

if __name__ == "__main__":
    asyncio.run(run_stream_simulation())
