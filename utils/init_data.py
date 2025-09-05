import os
import json

def ensure_data_files():
    # Create the data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Define each file and its default content
    files = {
        "suggestions.json": {},
        "player_stats.json": {},
        "active_players.json": {},
        "sudo_ids.json": []
    }

    # Initialize missing files with their defaults
    for name, default in files.items():
        path = os.path.join("data", name)
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default, f, indent=2)
