import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN      = os.getenv("BOT_TOKEN")
OWNER_ID       = int(os.getenv("OWNER_ID", "123456789"))
# initial sudo list; dynamic commands will update data/sudo_ids.json
SUDO_IDS       = [OWNER_ID]

DEFAULT_TIMER     = 20
MIN_WORD_LENGTH   = 3
