import logging
from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /userinfo to get your details.")


async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    user_info = f"""
*User Info:*
• Full Name: {user.full_name}
• Username: @{user.username if user.username else 'N/A'}
• User ID: `{user.id}`
• Language Code: {user.language_code if user.language_code else 'N/A'}
• Chat Type: {chat.type}
"""

    # Check admin status if in a group/supergroup
    if chat.type in ['group', 'supergroup']:
        try:
            member: ChatMember = await context.bot.get_chat_member(chat.id, user.id)
            status = member.status
            if status in ['administrator', 'creator']:
                user_info += f"• Admin Status: {status.capitalize()}\n"
            else:
                user_info += "• Admin Status: Not an admin\n"
        except Exception as e:
            user_info += f"• Admin Status: Unknown (error: {e})\n"

    await update.message.reply_markdown(user_info)


if __name__ == '__main__':
    BOT_TOKEN = "8187622361:AAGY9GYcS40i8tbGtQllMO4wRRVbL7zKv-U"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("userinfo", userinfo))

    print("Bot is running...")
    app.run_polling()
