import json
from telegram.ext import CommandHandler
from core.dictionary import save_word
from utils.access_control import is_admin

SUG_FILE = "data/suggestions.json"

def load_suggestions():
    try:
        with open(SUG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_suggestions(d):
    with open(SUG_FILE, "w") as f:
        json.dump(d, f, indent=2)

def suggest(update, context):
    if not context.args:
        return update.message.reply_text("❗ Usage: /suggest <word>")
    w = context.args[0].lower()
    d = load_suggestions()
    d[w] = update.effective_user.id
    save_suggestions(d)
    update.message.reply_text(f"📬 Suggested '{w}'")

def approve(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /approve <word>")
    w = context.args[0].lower()
    d = load_suggestions()
    if w in d:
        save_word(w)
        del d[w]
        save_suggestions(d)
        update.message.reply_text(f"✅ Approved '{w}'")
    else:
        update.message.reply_text("⚠️ Not in suggestions.")

def reject(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /reject <word>")
    w = context.args[0].lower()
    d = load_suggestions()
    if w in d:
        del d[w]
        save_suggestions(d)
        update.message.reply_text(f"❌ Rejected '{w}'")
    else:
        update.message.reply_text("⚠️ Not in suggestions.")

def suggestlist(update, context):
    d = load_suggestions()
    if not d:
        return update.message.reply_text("📭 No suggestions.")
    lines = [f"{w} by {uid}" for w, uid in d.items()]
    update.message.reply_text("📋 Suggestions:\n" + "\n".join(lines))

def register(dp):
    dp.add_handler(CommandHandler("suggest", suggest))
    dp.add_handler(CommandHandler("approve", approve))
    dp.add_handler(CommandHandler("reject", reject))
    dp.add_handler(CommandHandler("suggestlist", suggestlist))
