from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
import mysql_connector
import log_writer
TOKEN = "8026888580:AAFMK7XpRuuONw4KHCtLHy2r8WuAHZG5U2I"
CHOOSING, KEYWORD_INPUT = range(2)
# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    keyboard = [
        ["Key word search", "Year search"],
        ["Geners search", "Statistic search"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {user_first_name}!\nЭтот бот создан для выбора фильмов. Выбери один из вариантов:",
        reply_markup=reply_markup
    )
    return CHOOSING
# Обработка выбора меню
async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "Key word search":
        await update.message.reply_text("Введите ключевое слово:")
        return KEYWORD_INPUT
    elif choice == "Year search":
        await update.message.reply_text("Ты выбрал Вариант 2 :white_check_mark:")
    elif choice == "Geners search":
        await update.message.reply_text("Ты выбрал Вариант 3 :white_check_mark:")
    elif choice == "Statistic search":
        await update.message.reply_text("Ты выбрал Вариант 4 :white_check_mark:")
    else:
        await update.message.reply_text("Я не понял, выбери один из пунктов меню.")
    return CHOOSING
# Ввод ключевого слова
async def keyword_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key_word = update.message.text
    offset = 0
    result = sql_connector.find_by_key_word(key_word, offset)
    log_writer.log_query("keyword", {"key_word": key_word}, len(result))
    if result:
        await update.message.reply_text(result[0])
    else:
        await update.message.reply_text("Ничего не найдено.")
    return CHOOSING
# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_choice)],
            KEYWORD_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_search)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)
    print("Бот запущен...")
    app.run_polling()