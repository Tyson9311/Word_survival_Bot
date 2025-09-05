from telegram.ext import CommandHandler
from utils.access_control import is_admin
from core.game_session import sessions

def settimer(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    if not context.args or not context.args[0].isdigit():
        return update.message.reply_text("❗ Usage: /settimer <seconds>")
    sec = int(context.args[0])
    s = sessions.get(update.effective_chat.id)
    if s:
        s.timer = sec
        update.message.reply_text(f"⏱️ Timer set to {sec}s")
    else:
        update.message.reply_text("⚠️ No game.")

def setminlength(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    if not context.args or not context.args[0].isdigit():
        return update.message.reply_text("❗ Usage: /setminlength <n>")
    n = int(context.args[0])
    s = sessions.get(update.effective_chat.id)
    if s:
        s.min_length = n
        update.message.reply_text(f"🔠 Min length set to {n}")
    else:
        update.message.reply_text("⚠️ No game.")

def enablefreemode(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    s = sessions.get(update.effective_chat.id)
    if s:
        s.allow_free = True
        update.message.reply_text("✅ Free mode enabled.")
    else:
        update.message.reply_text("⚠️ No game.")

def disablefreemode(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    s = sessions.get(update.effective_chat.id)
    if s:
        s.allow_free = False
        update.message.reply_text("✅ Reply-only mode enabled.")
    else:
        update.message.reply_text("⚠️ No game.")

def register(dp):
    dp.add_handler(CommandHandler("settimer", settimer))
    dp.add_handler(CommandHandler("setminlength", setminlength))
    dp.add_handler(CommandHandler("enablefreemode", enablefreemode))
    dp.add_handler(CommandHandler("disablefreemode", disablefreemode))
