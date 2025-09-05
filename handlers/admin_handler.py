from telegram.ext import CommandHandler
from utils.access_control import is_admin, load_sudo, save_sudo
from core.game_session import force_stop

def forbban(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /botban <user_id>")
    uid = int(context.args[0])
    from data.banned_users import ban_user  # implement if needed
    ban_user(uid)
    update.message.reply_text(f"🔒 User {uid} banned.")

def forcestop(update, context):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Not authorized.")
    res = force_stop(update.effective_chat.id, update.effective_user.id)
    update.message.reply_text(res)

def addsudo(update, context):
    if update.effective_user.id != update.bot.owner_id:
        return update.message.reply_text("🚫 Only owner.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /addsudo <user_id>")
    uid = int(context.args[0])
    ids = load_sudo()
    if uid not in ids:
        ids.append(uid)
        save_sudo(ids)
        update.message.reply_text(f"✅ Sudo {uid} added.")
    else:
        update.message.reply_text("⚠️ Already sudo.")

def rmsudo(update, context):
    if update.effective_user.id != update.bot.owner_id:
        return update.message.reply_text("🚫 Only owner.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /rmsudo <user_id>")
    uid = int(context.args[0])
    ids = load_sudo()
    if uid in ids:
        ids.remove(uid)
        save_sudo(ids)
        update.message.reply_text(f"🗑️ Sudo {uid} removed.")
    else:
        update.message.reply_text("⚠️ Not a sudo.")

def sudolist(update, context):
    if update.effective_user.id != update.bot.owner_id:
        return update.message.reply_text("🚫 Only owner.")
    ids = load_sudo()
    update.message.reply_text("🔐 Sudo Users:\n" + "\n".join(map(str, ids)))

def register(dp):
    dp.add_handler(CommandHandler("botban", forbban))
    dp.add_handler(CommandHandler("forcestop", forcestop))
    dp.add_handler(CommandHandler("addsudo", addsudo))
    dp.add_handler(CommandHandler("rmsudo", rmsudo))
    dp.add_handler(CommandHandler("sudolist", sudolist))
