from datetime import datetime, timezone

from data.messages import THANK_YOU_MESSAGE
from data.survey_1_questions import question_list
from db.init import SessionLocal
from db.models import Answer, User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

USER_DATA_KEY = "survey_1_data"
QUESTION_INDEX = "survey_1_index"

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[USER_DATA_KEY] = {}
    context.user_data[QUESTION_INDEX] = 0
    return await ask_next_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question):
    text = question["question"]

    if question["type"] in ["single_choice", "multiple_choice"]:
        options = [[opt] for opt in question["options"]]
        await update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True, resize_keyboard=True)
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardRemove()
        )

async def save_user_and_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()

    telegram_id = str(update.effective_user.id)
    username = update.effective_user.username or ""

    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()

    for q in question_list:
        key = q["key"]
        answer_value = context.user_data[USER_DATA_KEY].get(key)
        if answer_value is None:
            continue
        answer = Answer(
            user_id=user.id,
            question=q["question"],
            answer=answer_value,
            timestamp=datetime.now(timezone.utc)
        )
        session.add(answer)

    session.commit()
    session.close()

async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data[QUESTION_INDEX]
    
    if idx >= len(question_list):
        await save_user_and_answers(update, context)
        await update.message.reply_text(THANK_YOU_MESSAGE, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    await send_question(update, context, question_list[idx])
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
