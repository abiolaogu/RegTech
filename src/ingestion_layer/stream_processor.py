from typing import Dict, Any
import asyncio

# Mock FastStream behavior since I cannot install the actual broker locally easily without docker
# In a real scenario: from faststream import FastStream, Logger
# from faststream.kafka import KafkaBroker

class MockFastStreamFunc:
    def __init__(self):
        self.handlers = {}

    def subscriber(self, topic: str):
        def decorator(func):
            self.handlers[topic] = func
            return func
        return decorator

    async def emit(self, topic: str, msg: Dict[str, Any]):
        if topic in self.handlers:
            print(f"[STREAM] Processing event on topic '{topic}': {msg}")
            # In real life this is async
            await self.handlers[topic](msg)
        else:
            print(f"[STREAM] No handler for topic '{topic}'")

broker = MockFastStreamFunc()

# --- Telecom Connector (CDR Parsing) ---
@broker.subscriber("telecom.cdr")
async def handle_cdr(msg: Dict[str, Any]):
    # Logic: Parse CDR, check for QoS drops?
    # Simulating ASN.1 decoding
    call_duration = msg.get("duration", 0)
    drop_reason = msg.get("termination_code")
    
    if drop_reason == "RADIO_LINK_FAILURE":
        print(f"  -> ALERT: Dropped Call detected! Duration: {call_duration}s")
        # Could trigger the Board Advisory Module here

# --- Banking Connector (ISO 8583 Stream) ---
@broker.subscriber("banking.tx")
async def handle_banking_tx(msg: Dict[str, Any]):
    # Logic: Monitor for AML
    amount = msg.get("amount", 0)
    if amount > 5_000_000:
        print(f"  -> AML FLAG: High Value Transaction Detected: N{amount}")
        # Could call CBN Module here

# --- Simulation Runner ---
async def run_stream_simulation():
    print("--- Starting High-Performance Stream Simulation ---")
    
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

if __name__ == "__main__":
    asyncio.run(run_stream_simulation())
