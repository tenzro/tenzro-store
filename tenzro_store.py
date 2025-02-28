import os
import json
import shutil
import threading
from typing import Any, Dict, Optional

class TenzroStore:
    """
    Tenzro Store: A modular storage system for the Tenzro Ledger Framework.
    Provides thread-safe key-value storage with replication capabilities, using .tzds files.
    
    Args:
        base_dir (str): Base directory for storing .tzds files
        node_id (str): Unique identifier for this storage node
    
    Example:
        >>> store = TenzroStore(base_dir="my_store", node_id="node1")
        >>> store.put("tx1", {"transaction_id": "tx1", "amount": 100})
        >>> data = store.get("tx1")
    """
    
    FILE_EXTENSION = ".tzds"  # Tenzro Data Store file extension
    
    def __init__(self, base_dir: str, node_id: str):
        self.base_dir = base_dir
        self.node_id = node_id
        self.index: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        os.makedirs(base_dir, exist_ok=True)
        self._load_index()

    def _load_index(self) -> None:
        """Load existing .tzds files from storage directory into index."""
        for filename in os.listdir(self.base_dir):
            if filename.endswith(self.FILE_EXTENSION):
                filepath = os.path.join(self.base_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    key = filename[:-len(self.FILE_EXTENSION)]  # Strip .tzds extension
                    self.index[key] = data

    def put(self, key: str, value: Dict[str, Any]) -> str:
        """
        Store data with the given key in a .tzds file.
        
        Args:
            key (str): Unique key for the data
            value (Dict[str, Any]): Data to store
            
        Returns:
            str: The key used for storage
        """
        with self.lock:
            self.index[key] = value
            filepath = os.path.join(self.base_dir, f"{key}{self.FILE_EXTENSION}")
            with open(filepath, 'w') as f:
                json.dump(value, f)
            return key

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data by key from the index.
        
        Args:
            key (str): Key to look up
            
        Returns:
            Optional[Dict[str, Any]]: Stored data or None if not found
        """
        with self.lock:
            return self.index.get(key)

    def replicate_to(self, target_dir: str) -> None:
        """
        Replicate all .tzds files to a target directory.
        
        Args:
            target_dir (str): Directory to replicate data to
        """
        with self.lock:
            os.makedirs(target_dir, exist_ok=True)
            for key, value in self.index.items():
                filepath = os.path.join(target_dir, f"{key}{self.FILE_EXTENSION}")
                with open(filepath, 'w') as f:
                    json.dump(value, f)

    def clear(self) -> None:
        """Clear all data from the store, removing all .tzds files."""
        with self.lock:
            self.index.clear()
            for filename in os.listdir(self.base_dir):
                if filename.endswith(self.FILE_EXTENSION):
                    os.remove(os.path.join(self.base_dir, filename))