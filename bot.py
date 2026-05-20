from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import init_db, save_message, get_user_history, save_user_style, get_user_style, get_search_history
from ai_handler import ask_claude, analyze_user_style
from search_handler import google_search, format_results
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "هلا وغلا! 👋\nأنا بوتك العراقي الذكي\n\nالأوامر:\n/search كلمة — تبحث بـ Google\n/searches — تاريخ بحوثك\n/history — تاريخ محادثتك"
    )

async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    history = get_user_history(user.id, limit=5)
    if not history:
        await update.message.reply_text("بعد ما عندك رسائل محفوظة 📭")
        return
    text = "🗂️ آخر رسائلك:\n\n"
    for msg, time in history:
        text += f"🕐 {time[:16]}\n💬 {msg}\n\n"
    await update.message.reply_text(text)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if not context.args:
        await update.message.reply_text("اكتب شنو تبحث — مثلاً:\n/search برمجة بايثون")
        return
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 أبحث عن: {query}")
    await update.message.chat.send_action("typing")
    results = google_search(query)
    reply = format_results(results, query, user.id)
    await update.message.reply_text(reply)

async def searches_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    history = get_search_history(user.id)
    if not history:
        await update.message.reply_text("بعد ما سويت أي بحث 📭")
        return
    text = "📚 آخر بحوثك:\n\n"
    for query, _, time in history:
        text += f"🕐 {time[:16]}\n🔍 {query}\n\n"
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    save_message(user.id, user.username, text)
    history = get_user_history(user.id, limit=10)
    user_style = get_user_style(user.id)
    if len(history) % 5 == 0 and len(history) > 0:
        new_style = analyze_user_style(history)
        save_user_style(user.id, new_style)
        user_style = new_style
    await update.message.chat.send_action("typing")
    reply = ask_claude(text, history, user_style)
    await update.message.reply_text(reply)

init_db()
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("history", history_cmd))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("searches", searches_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
