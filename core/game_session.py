import time, random, json
from core.mode_engine import get_random_mode, validate_word, load_categories
from core.dictionary import is_valid_word
from core.timer_visuals import generate_timer_bar
from config import DEFAULT_TIMER, MIN_WORD_LENGTH
from utils.access_control import load_sudo
from utils.init_data import ensure_data_files

sessions = {}        # chat_id → GameSession
active_players = {}  # user_id → chat_id lock

class GameSession:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = {}           # user_id → {"name", "score"}
        self.order = []
        self.started = False
        self.current_index = 0
        self.current_mode = None
        self.last_word = ""
        self.turn_start = None
        self.timer = DEFAULT_TIMER
        self.min_length = MIN_WORD_LENGTH

    def add_player(self, user_id, name):
        if self.started:
            return "🚫 Game already started."
        if user_id in active_players:
            return "🚫 Already in another game."
        self.players[user_id] = {"name": name, "score": 0}
        active_players[user_id] = self.chat_id
        return f"✅ {name} joined."

    def exit_lobby(self, user_id):
        if self.started:
            return "🚫 Game already started."
        if user_id in self.players:
            del self.players[user_id]
            del active_players[user_id]
            return "👋 You left."
        return "⚠️ You’re not in lobby."

    def force_start(self):
        if self.started:
            return "⚠️ Already started."
        if not self.players:
            return "🚫 No players."
        self.started = True
        self.order = list(self.players.keys())
        random.shuffle(self.order)
        self.current_index = 0
        self.current_mode = get_random_mode()
        self.turn_start = time.time()
        return "⏩ Game force-started!"

    def force_stop(self):
        for uid in list(self.players):
            if uid in active_players:
                del active_players[uid]
        if self.chat_id in sessions:
            del sessions[self.chat_id]
        return "🛑 Game ended."

    def get_current_player(self):
        return self.order[self.current_index]

    def rotate_turn(self):
        self.current_index = (self.current_index + 1) % len(self.order)
        self.current_mode = get_random_mode()
        self.turn_start = time.time()

    def get_turn_context(self):
        cats = load_categories()
        cat = random.choice(list(cats.keys()))
        return {
            "last_letter": self.last_word[-1] if self.last_word else "",
            "last_length": len(self.last_word),
            "category": cat,
            "category_words": cats.get(cat, []),
            "banned_letter": random.choice("abcdefghijklmnopqrstuvwxyz")
        }

    def submit_word(self, user_id, word):
        if user_id != self.get_current_player():
            return "⏳ Wait your turn."
        if not word or not word.strip():
            return "❗ Submit a non-empty word."
        elapsed = time.time() - self.turn_start
        if elapsed > self.timer:
            self.rotate_turn()
            return "⌛ Time up."
        if len(word) < self.min_length:
            return f"❌ Too short\n{generate_timer_bar(self.timer - elapsed, self.timer)}"
        if not is_valid_word(word):
            return f"❌ Invalid\n{generate_timer_bar(self.timer - elapsed, self.timer)}"
        ctx = self.get_turn_context()
        if not validate_word(self.current_mode, word, ctx):
            return f"❌ Doesn’t match {self.current_mode}\n" + \
                   generate_timer_bar(self.timer - elapsed, self.timer)
        # Score
        pts = 10 + (5 if len(word) > 7 else 0)
        if self.current_mode == "snake":
            pts += 3
        if self.current_mode == "category":
            pts += 5
        self.players[user_id]["score"] += pts
        self.last_word = word.lower()
        self.rotate_turn()
        return f"✅ '{word}' +{pts} pts"

    def get_score(self, user_id):
        return self.players.get(user_id, {}).get("score", 0)

    def get_leaderboard(self):
        board = sorted(self.players.items(),
                       key=lambda x: x[1]["score"], reverse=True)
        return "\n".join(f"{data['name']}: {data['score']} pts"
                         for uid, data in board)

# session management

def create_session(chat_id):
    sessions[chat_id] = GameSession(chat_id)

def add_player(chat_id, user_id, name):
    s = sessions.get(chat_id)
    return s.add_player(user_id, name) if s else "⚠️ No game."

def exit_lobby(chat_id, user_id):
    s = sessions.get(chat_id)
    return s.exit_lobby(user_id) if s else "⚠️ No game."

def force_start(chat_id, user_id):
    s = sessions.get(chat_id)
    return s.force_start() if s else "⚠️ No game."

def force_stop(chat_id, user_id):
    s = sessions.get(chat_id)
    return s.force_stop() if s else "⚠️ No game."

def submit_word(chat_id, user_id, word):
    s = sessions.get(chat_id)
    return s.submit_word(user_id, word) if s else "⚠️ No game."

def get_score(chat_id, user_id):
    s = sessions.get(chat_id)
    return s.get_score(user_id) if s else 0

def get_leaderboard(chat_id):
    s = sessions.get(chat_id)
    return s.get_leaderboard() if s else "⚠️ No game."
