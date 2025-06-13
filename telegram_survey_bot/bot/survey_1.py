from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from data.survey_1_questions import question_list

USER_DATA_KEY = "survey_1_data"
QUESTION_INDEX = "survey_1_index"

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[USER_DATA_KEY] = {}
    context.user_data[QUESTION_INDEX] = 0
    return await ask_next_question(update, context)

async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data[QUESTION_INDEX]
    if idx >= len(question_list):
        # All questions done
        answers = context.user_data[USER_DATA_KEY]
        await update.message.reply_text("Thank you! Your answers:\n" + str(answers), reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    q = question_list[idx]
    text = q["question"]
    if q["type"] in ["single_choice", "multiple_choice"]:
        options = [[opt] for opt in q["options"]]
        await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True, resize_keyboard=True))
    else:
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    return 1

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data[QUESTION_INDEX]
    q = question_list[idx]
    key = q["key"]
    answer = update.message.text
    context.user_data[USER_DATA_KEY][key] = answer
    context.user_data[QUESTION_INDEX] += 1
    return await ask_next_question(update, context)

survey_1_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^survey_1$"), start_survey)],
    states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)]},
    fallbacks=[]
)
