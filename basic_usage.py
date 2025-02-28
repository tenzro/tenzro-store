from tenzro_store import TenzroStore

# Initialize a store instance
store = TenzroStore(base_dir="ledger_data", node_id="node1")

# Store a transaction
transaction = {
    "transaction_id": "tx_123",
    "metadata": {"project": "test", "timestamp": "2025-02-28"},
    "payload": {"amount": 100, "currency": "USD"}
}
store.put("tx_123", transaction)

# Retrieve the transaction
data = store.get("tx_123")
print(f"Retrieved: {data}")

# Replicate to a follower node
store.replicate_to("follower_data")