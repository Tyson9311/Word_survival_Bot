from telegram.ext import CommandHandler
from core.dictionary import save_word, remove_word, is_valid_word, load_words

def add_word(update, context):
    if not context.args:
        return update.message.reply_text("❗ Usage: /addword <word>")
    w = context.args[0]
    ok = save_word(w)
    update.message.reply_text(f"✅ '{w}' added." if ok else f"⚠️ '{w}' exists.")

def rm_word(update, context):
    if not context.args:
        return update.message.reply_text("❗ Usage: /rmword <word>")
    w = context.args[0]
    ok = remove_word(w)
    update.message.reply_text(f"🗑️ '{w}' removed." if ok else f"⚠️ '{w}' not found.")

def exist_word(update, context):
    if not context.args:
        return update.message.reply_text("❗ Usage: /exist <word>")
    w = context.args[0]
    ex = is_valid_word(w)
    update.message.reply_text(f"✅ '{w}' exists." if ex else f"❌ '{w}' not found.")

def word_count(update, context):
    cnt = len(load_words())
    update.message.reply_text(f"📚 Total words: {cnt}")

def register(dp):
    dp.add_handler(CommandHandler("addword", add_word))
    dp.add_handler(CommandHandler("rmword", rm_word))
    dp.add_handler(CommandHandler("exist", exist_word))
    dp.add_handler(CommandHandler("wordcount", word_count))
