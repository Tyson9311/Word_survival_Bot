from telegram.ext import CommandHandler, MessageHandler, Filters
from core.game_session import (
    create_session, add_player, exit_lobby,
    force_start, submit_word
)
from utils.message_builder import build_turn_prompt

def start_game(update, context):
    create_session(update.effective_chat.id)
    update.message.reply_text("🎮 New game! Use /join to enter.")

def join_game(update, context):
    user = update.effective_user
    res = add_player(update.effective_chat.id, user.id, user.first_name)
    update.message.reply_text(res)

def exit_game(update, context):
    res = exit_lobby(update.effective_chat.id, update.effective_user.id)
    update.message.reply_text(res)

def forcestart(update, context):
    res = force_start(update.effective_chat.id, update.effective_user.id)
    update.message.reply_text(res)

def handle_submission(update, context):
    if not update.message.text:
        return
    res = submit_word(
        update.effective_chat.id,
        update.effective_user.id,
        update.message.text
    )
    update.message.reply_text(res)

def register(dp):
    dp.add_handler(CommandHandler("startgame", start_game))
    dp.add_handler(CommandHandler("join", join_game))
    dp.add_handler(CommandHandler("exit", exit_game))
    dp.add_handler(CommandHandler("forcestart", forcestart))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_submission))
