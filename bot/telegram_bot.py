print('BEGIN IMPORT')

import logging
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TG_BOT_TOKEN
from core.application import Application
from config import REQUIREMENTS_HEADERS

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне csv файл, и я его проверю")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        tmp_path = tmp.name

    app = Application(tmp_path, requirements_headers=REQUIREMENTS_HEADERS)

    class Args:
        no_db = True
        json = True
        file_path = tmp_path

    validation_result, exit_code, db_result = app.run(Args())

    if Args.json:
        from report.console_reporter_json import ConsoleReporterJSON
        reporter = ConsoleReporterJSON()
    else:
        from report.console_reporter import ConsoleReporter
        reporter = ConsoleReporter()

    reporter.print_report(validation_result, db_result)

    await update.message.reply_text(str(reporter.json_data))

def run_bot():
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    app.run_polling()

if __name__ == "__main__":
    run_bot()