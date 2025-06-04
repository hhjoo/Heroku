from telegram import (
    Update,
    LabeledPrice,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    PreCheckoutQueryHandler,
)
import logging
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_PROVIDER_TOKEN = os.getenv('TEST_PROVIDER_TOKEN')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    prices = [LabeledPrice("خدمة تجريبية", 1000)]
    await context.bot.send_invoice(
        chat_id=chat_id,
        title="خدمة نجوم تجريبية",
        description="دفع 1000 نجمة ثم استرجاعها تلقائيًا (وهميًا)",
        payload="test-payload",
        provider_token=TEST_PROVIDER_TOKEN,
        currency="USD",
        prices=prices,
        start_parameter="test-payment",
        need_name=True
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.successful_payment.total_amount / 100
    await update.message.reply_text(f"✅ تم الدفع بنجاح: {amount:.2f} دولار 💸")
    await update.message.reply_text("🔁 يتم الآن إرجاع النجوم إليك تلقائيًا (وهميًا)...")
    await update.message.reply_text(f"✅ تم إرجاع {amount:.2f} دولار (1000 نجمة) بنجاح!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("🚀 Bot is running...")
    app.run_polling()
