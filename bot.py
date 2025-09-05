from telegram.ext import Updater
from handlers import (
    game_handler, dictionary_handler, admin_handler,
    suggestion_handler, settings_handler, score_handler
)
from config import BOT_TOKEN
from utils.init_data import ensure_data_files

def main():
    ensure_data_files()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    game_handler.register(dp)
    dictionary_handler.register(dp)
    admin_handler.register(dp)
    suggestion_handler.register(dp)
    settings_handler.register(dp)
    score_handler.register(dp)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
