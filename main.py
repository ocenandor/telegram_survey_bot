import logging
import os

from bot.main_menu import start
from bot.survey_1 import survey_1_conv_handler
from db.init import init_db
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")


def main():
    init_db()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(survey_1_conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
