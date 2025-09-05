from telegram.ext import CommandHandler
from core.game_session import get_score, get_leaderboard

def score(update, context):
    val = get_score(update.effective_chat.id, update.effective_user.id)
    update.message.reply_text(f"🏅 Your score: {val}")

def leaderboard(update, context):
    board = get_leaderboard(update.effective_chat.id)
    update.message.reply_text("📊 Leaderboard:\n" + board)

def stats(update, context):
    # Extend using data/player_stats.json if implemented
    update.message.reply_text("ℹ️ Player stats coming soon.")

def register(dp):
    dp.add_handler(CommandHandler("score", score))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("stats", stats))
