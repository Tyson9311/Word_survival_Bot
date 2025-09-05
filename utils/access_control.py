from config import OWNER_ID
import json, os

SUDO_FILE = "data/sudo_ids.json"

def load_sudo():
    try:
        with open(SUDO_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_sudo(ids):
    with open(SUDO_FILE, "w") as f:
        json.dump(ids, f, indent=2)

def is_owner(user_id):
    return user_id == OWNER_ID

def is_sudo(user_id):
    return user_id in load_sudo()

def is_admin(user_id):
    return is_owner(user_id) or is_sudo(user_id)
