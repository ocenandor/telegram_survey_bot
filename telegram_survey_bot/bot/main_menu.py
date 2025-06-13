from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

MAIN_MENU_OPTIONS = [["survey_1"], ["other_function_1", "other_function_2"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Choose a function:",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU_OPTIONS, one_time_keyboard=True, resize_keyboard=True)
    )
