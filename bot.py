import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get token from environment variable (or replace directly with your token)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT-YOUR-BOT-TOKEN-HERE")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a file and I’ll give you a direct download link!")

# Handle any file/document
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    photo = update.message.photo

    if document:  # if it's a document
        file_id = document.file_id
    elif photo:   # if it's a photo (take the best quality one)
        file_id = photo[-1].file_id
    else:
        await update.message.reply_text("❌ Unsupported file type.")
        return

    # Get file info from Telegram
    file = await context.bot.get_file(file_id)

    # Create direct link
    download_link = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"

    await update.message.reply_text(f"✅ Here’s your direct link:\n{download_link}")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    app.run_polling()

if __name__ == "__main__":
    main()
