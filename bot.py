from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Falta BOT_TOKEN")

USDT_LINK = "https://s.binance.com/iXbyQcVL"
BTC_LINK = "https://s.binance.com/xuzlIvp2"
SUPPORT_EMAIL = "toc.services.requests@gmail.com"
SUPPORT_TELEGRAM = "@bermeloh2"
QR_CRYPTO = "qr.png"
QR_CASHAPP = "qr2.png"

BUY_WORDS = [
    "buy", "access", "pay", "join", "subscribe",
    "enter", "price", "cost", "membership", "premium", "vip",
    "get access", "full access", "how do i join", "how can i join",
    "how to join", "how can i enter", "register", "sign up",
    "comprar", "acceso", "pagar", "unirme", "precio",
    "costo", "membresia", "membresía", "registrarme",
    "como entrar", "cómo entrar", "como me uno", "cómo me uno",
    "como unirme", "cómo unirme", "quiero entrar",
    "quiero acceso", "quiero unirme"
]

CRYPTO_WORDS = [
    "crypto", "btc", "usdt", "binance", "bitcoin",
    "cripto", "crypto payment", "pago cripto"
]

HELP_WORDS = [
    "help", "support", "problem", "issue",
    "ayuda", "soporte", "problema", "error",
    "cloud", "nube"
]

MEMBER_WORDS = [
    "member", "already member", "i am member",
    "miembro", "ya soy miembro", "soy miembro"
]

CASHAPP_WORDS = [
    "cashapp", "cash app", "cash", "zelle", "usd", "dollars",
    "pagar con cash", "pago en dolares", "dólares", "dolares"
]


def contains_any(text: str, words: list) -> bool:
    return any(word in text for word in words)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Buy Access", callback_data="buy")],
        [InlineKeyboardButton("💎 Crypto Payment", callback_data="crypto")],
        [InlineKeyboardButton("💵 CashApp Payment", callback_data="cashapp")],
        [InlineKeyboardButton("🆘 Support", callback_data="help")],
        [InlineKeyboardButton("✅ I am a Member", callback_data="member")],
    ])


def buy_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Pay 99.99 USDT", url=USDT_LINK)],
        [InlineKeyboardButton("₿ Pay with BTC", url=BTC_LINK)],
        [InlineKeyboardButton("💎 Crypto Payment Info", callback_data="crypto")],
        [InlineKeyboardButton("🆘 Support", callback_data="help")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


async def send_welcome(target):
    await target.reply_text(
        "🔥 UNLOCK FULL ACCESS NOW\n\n"
        "Private content. Instant access. Crypto payment.\n\n"
        "💳 Price: 99.99\n\n"
        "Choose an option below:",
        reply_markup=main_menu_keyboard()
    )


async def send_buy(target):
    text = (
        "🚀 FULL ACCESS AVAILABLE\n\n"
        "💳 Price: 99.99\n\n"
        "Choose your payment method:\n\n"
        "💰 USDT (recommended)\n"
        "₿ BTC available\n\n"
        "📲 Scan the QR or use the buttons below.\n\n"
        "⚠️ IMPORTANT:\n"
        "After payment, send screenshot + details to:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 {SUPPORT_TELEGRAM}"
    )
    with open("qr.png", "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=buy_keyboard()
        )


async def send_crypto(target):
    text = (
        "💎 CRYPTO PAYMENT METHODS\n\n"
        "Available options:\n\n"
        "💰 USDT (fast & recommended)\n"
        f"{USDT_LINK}\n\n"
        "₿ BTC\n"
        f"{BTC_LINK}\n\n"
        "📲 You can also scan the QR image.\n\n"
        "⚠️ After payment, send screenshot + details to:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 {SUPPORT_TELEGRAM}"
    )
    with open("qr.png", "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=buy_keyboard()
        )


async def send_cashapp(target):
    text = (
        "💵 CASHAPP PAYMENT\n\n"
        "Price: $99.99 USD\n\n"
        "📲 Scan the QR code with your CashApp to pay.\n\n"
        "⚠️ IMPORTANT:\n"
        "After payment, send screenshot + details to:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 {SUPPORT_TELEGRAM}"
    )
    with open(QR_CASHAPP, "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 Crypto Payment Instead", callback_data="crypto")],
                [InlineKeyboardButton("🆘 Support", callback_data="help")],
                [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
            ])
        )


async def send_help(target):
    text = (
        "🆘 SUPPORT\n\n"
        "If you need help, contact us:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 Telegram: {SUPPORT_TELEGRAM}\n\n"
        "⚠️ IMPORTANT — Include this info:\n"
        "• TOC Username\n"
        "• TOC2.Cloud Email\n"
        "• Detailed description of your issue\n\n"
        "📌 Support available for:\n"
        "• Cloud activations\n"
        "• Membership issues\n"
        "• Payment verification\n"
        "• Account access problems\n\n"
        "🚀 Fastest support via Telegram (recommended)\n\n"
        "The more details you provide, the faster we can help you."
    )
    await target.reply_text(text, reply_markup=main_menu_keyboard())


async def send_member(target):
    text = (
        "✅ MEMBER SUPPORT\n\n"
        "Already a member?\n\n"
        "For faster assistance, contact:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 Telegram: {SUPPORT_TELEGRAM}\n\n"
        "⚠️ Please include:\n"
        "• TOC Username\n"
        "• TOC2.Cloud Email\n"
        "• Membership type\n"
        "• Detailed description of the problem\n\n"
        "📌 Basic validation before contacting support:\n"
        "• Check that your TOC email and TOC2.Cloud email match\n"
        "• Confirm your payment was completed\n"
        "• Verify if the issue is cloud activation, membership access, or payment verification\n\n"
        "The more complete your info is, the faster support can help you."
    )
    await target.reply_text(text, reply_markup=main_menu_keyboard())


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[START] user={user.id} username={user.username}")
    await send_welcome(update.message)


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = query.data
    print(f"[BUTTON] user={user.id} username={user.username} action={data}")

    if data == "buy":
        await send_buy(query.message)
    elif data == "crypto":
        await send_crypto(query.message)
    elif data == "cashapp":
        await send_cashapp(query.message)
    elif data == "help":
        await send_help(query.message)
    elif data == "member":
        await send_member(query.message)
    elif data == "menu":
        await send_welcome(query.message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    text = update.message.text.lower().strip()

    print(f"[MSG] user={user.id} username={user.username} text={text}")

    if contains_any(text, BUY_WORDS):
        await send_buy(update.message)
    elif contains_any(text, CRYPTO_WORDS):
        await send_crypto(update.message)
    elif contains_any(text, CASHAPP_WORDS):
        await send_cashapp(update.message)
    elif contains_any(text, MEMBER_WORDS):
        await send_member(update.message)
    elif contains_any(text, HELP_WORDS):
        await send_help(update.message)
    else:
        await send_welcome(update.message)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
