from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("Falta BOT_TOKEN")

USDT_LINK = "https://s.binance.com/iXbyQcVL"
BTC_LINK = "https://s.binance.com/xuzlIvp2"
CANDIDVERSE_49_LINK = "https://s.binance.com/ALQ8lAU1"
CANDIDVERSE_99_LINK = "https://s.binance.com/qWgp2YND"

SUPPORT_EMAIL = "toc.services.requests@gmail.com"
SUPPORT_TELEGRAM = "@bermeloh2"

QR_CRYPTO = "qr.png"
QR_CASHAPP = "qr2.png"

# Estados simples en memoria
# paid flow: method -> username -> email -> screenshot -> extra
# support flow: category -> username -> email -> details
user_states = {}


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

CASHAPP_WORDS = [
    "cashapp", "cash app", "cash"
]

HELP_WORDS = [
    "help", "support", "problem", "issue",
    "ayuda", "soporte", "problema", "error",
    "cloud", "nube"
]


def contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)


def safe_username(user) -> str:
    return f"@{user.username}" if user.username else "No username"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Buy Access", callback_data="buy")],
        [InlineKeyboardButton("✅ I Already Paid", callback_data="already_paid")],
        [InlineKeyboardButton("💎 Crypto Payment", callback_data="crypto")],
        [InlineKeyboardButton("💵 CashApp Payment", callback_data="cashapp")],
        [InlineKeyboardButton("🌐 THECANDIDVERSE.COM", callback_data="candidverse")],
        [InlineKeyboardButton("🆘 Support", callback_data="help")],
    ])


def buy_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Pay 99.99 USDT", url=USDT_LINK)],
        [InlineKeyboardButton("₿ Pay with BTC", url=BTC_LINK)],
        [InlineKeyboardButton("✅ I Already Paid", callback_data="already_paid")],
        [InlineKeyboardButton("💵 CashApp Payment", callback_data="cashapp")],
        [InlineKeyboardButton("🆘 Support", callback_data="help")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def cashapp_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ I Already Paid", callback_data="already_paid")],
        [InlineKeyboardButton("💎 Crypto Payment Instead", callback_data="crypto")],
        [InlineKeyboardButton("🆘 Support", callback_data="help")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def candidverse_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Buy 5 Videos - $49.99", url=CANDIDVERSE_49_LINK)],
        [InlineKeyboardButton("🚀 Buy 10 Videos - $99.99", url=CANDIDVERSE_99_LINK)],
        [InlineKeyboardButton("📩 Support", callback_data="help")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def paid_method_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 USDT", callback_data="paid_method_usdt")],
        [InlineKeyboardButton("₿ BTC", callback_data="paid_method_btc")],
        [InlineKeyboardButton("💵 CashApp", callback_data="paid_method_cashapp")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def support_category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("☁ Cloud activation", callback_data="support_cat_cloud")],
        [InlineKeyboardButton("👤 Membership issue", callback_data="support_cat_membership")],
        [InlineKeyboardButton("💳 Payment verification", callback_data="support_cat_payment")],
        [InlineKeyboardButton("🔐 Access problem", callback_data="support_cat_access")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_flow")],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="menu")],
    ])


def clear_user_state(user_id: int):
    if user_id in user_states:
        del user_states[user_id]


async def notify_admin_text(context: ContextTypes.DEFAULT_TYPE, text: str):
    if not ADMIN_CHAT_ID:
        return
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    except Exception as e:
        print(f"[ADMIN TEXT ERROR] {e}")


async def notify_admin_photo(context: ContextTypes.DEFAULT_TYPE, photo_file_id: str, caption: str):
    if not ADMIN_CHAT_ID:
        return
    try:
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_file_id, caption=caption)
    except Exception as e:
        print(f"[ADMIN PHOTO ERROR] {e}")


async def send_welcome(target):
    await target.reply_text(
        "🔥 UNLOCK FULL ACCESS NOW\n\n"
        "Private content. Instant access. Crypto or CashApp payment.\n\n"
        "💳 Price: 99.99\n\n"
        "Choose an option below:",
        reply_markup=main_menu_keyboard()
    )


async def send_buy(target):
    text = (
        "💳 FULL ACCESS AVAILABLE\n\n"
        "Price: 99.99\n\n"
        "Choose your payment method:\n"
        "• USDT (recommended)\n"
        "• BTC\n"
        "• CashApp\n\n"
        "After payment, tap:\n"
        "✅ I Already Paid\n\n"
        "⚠️ IMPORTANT:\n"
        "Send screenshot + details for activation."
    )

    with open(QR_CRYPTO, "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=buy_keyboard()
        )


async def send_crypto(target):
    text = (
        "💎 CRYPTO PAYMENT\n\n"
        f"💰 USDT:\n{USDT_LINK}\n\n"
        f"₿ BTC:\n{BTC_LINK}\n\n"
        "After payment, tap:\n"
        "✅ I Already Paid"
    )

    with open(QR_CRYPTO, "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=buy_keyboard()
        )


async def send_cashapp(target):
    text = (
        "💵 CASHAPP PAYMENT\n\n"
        "Price: $99.99 USD\n\n"
        "Scan the QR code with your CashApp to pay.\n\n"
        "After payment, tap:\n"
        "✅ I Already Paid\n\n"
        "⚠️ IMPORTANT:\n"
        "After payment, send screenshot + details to:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 {SUPPORT_TELEGRAM}"
    )

    with open(QR_CASHAPP, "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=cashapp_keyboard()
        )


async def send_support_intro(target):
    await target.reply_text(
        "🆘 SUPPORT\n\n"
        "Choose your issue type below.\n\n"
        "If you are already a member, use:\n"
        "• Cloud activation\n"
        "• Membership issue\n"
        "• Payment verification\n"
        "• Access problem",
        reply_markup=support_category_keyboard()
    )


async def send_candidverse(target):
    text = (
        "🌐 THECANDIDVERSE.COM\n\n"
        "🔥 CUSTOM VIDEO ACCESS\n\n"
        "Choose your option:\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "💰 5 VIDEOS PACK\n"
        "Price: $49.99\n\n"
        "• No bundles accepted\n"
        "• You choose the videos\n"
        "• Send links after payment\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🚀 FULL ACCESS PACKAGE\n"
        "Price: $99.99\n\n"
        "• Up to 10 videos / links\n"
        "• Full custom selection\n"
        "• Priority processing\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "📩 AFTER PAYMENT\n\n"
        "Send your links or requests to:\n"
        f"📧 {SUPPORT_EMAIL}\n"
        f"📩 {SUPPORT_TELEGRAM}\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "⚠️ IMPORTANT\n\n"
        "• No bundles allowed\n"
        "• Only individual video selection\n"
        "• Requests without links may be delayed"
    )
    await target.reply_text(text, reply_markup=candidverse_keyboard())


async def start_paid_flow(target, user_id: int):
    user_states[user_id] = {
        "flow": "paid",
        "step": "method",
        "data": {}
    }
    await target.reply_text(
        "✅ PAYMENT CONFIRMATION\n\n"
        "Select the payment method you used:",
        reply_markup=paid_method_keyboard()
    )


async def start_support_flow(target, user_id: int):
    user_states[user_id] = {
        "flow": "support",
        "step": "category",
        "data": {}
    }
    await target.reply_text(
        "🆘 SUPPORT REQUEST\n\n"
        "Select your issue type:",
        reply_markup=support_category_keyboard()
    )


async def ask_paid_username(target):
    await target.reply_text(
        "Please send your TOC Username.",
        reply_markup=cancel_keyboard()
    )


async def ask_paid_email(target):
    await target.reply_text(
        "Please send your TOC2.Cloud Email.",
        reply_markup=cancel_keyboard()
    )


async def ask_paid_screenshot(target):
    await target.reply_text(
        "Now send your payment screenshot.\n\n"
        "You can send it as an image.",
        reply_markup=cancel_keyboard()
    )


async def ask_paid_extra(target):
    await target.reply_text(
        "Anything else we should know?\n\n"
        "If not, reply with:\n"
        "no",
        reply_markup=cancel_keyboard()
    )


async def finish_paid_flow(target, context: ContextTypes.DEFAULT_TYPE, user, user_id: int):
    data = user_states[user_id]["data"]

    summary = (
        "✅ PAYMENT CONFIRMATION RECEIVED\n\n"
        f"Payment method: {data.get('method', '-')}\n"
        f"TOC Username: {data.get('username', '-')}\n"
        f"TOC2.Cloud Email: {data.get('email', '-')}\n"
        f"Screenshot received: {data.get('screenshot', '-')}\n"
        f"Extra info: {data.get('extra', '-')}\n\n"
        "⏳ Status: Pending Review\n\n"
        "Your payment confirmation has been received and is now under review.\n"
        "Support will verify it and contact you if needed.\n\n"
        f"If urgent, also contact:\n📧 {SUPPORT_EMAIL}\n📩 {SUPPORT_TELEGRAM}"
    )

    admin_summary = (
        "🔥 NEW PAYMENT CONFIRMATION\n\n"
        f"User ID: {user.id}\n"
        f"Telegram: {safe_username(user)}\n"
        f"Payment method: {data.get('method', '-')}\n"
        f"TOC Username: {data.get('username', '-')}\n"
        f"TOC2.Cloud Email: {data.get('email', '-')}\n"
        f"Screenshot received: {data.get('screenshot', '-')}\n"
        f"Extra info: {data.get('extra', '-')}"
    )

    await target.reply_text(summary, reply_markup=main_menu_keyboard())
    await notify_admin_text(context, admin_summary)

    print(f"[PAID FLOW COMPLETE] user={user_id} data={data}")
    clear_user_state(user_id)


async def ask_support_username(target):
    await target.reply_text(
        "Please send your TOC Username.",
        reply_markup=cancel_keyboard()
    )


async def ask_support_email(target):
    await target.reply_text(
        "Please send your TOC2.Cloud Email.",
        reply_markup=cancel_keyboard()
    )


async def ask_support_details(target):
    await target.reply_text(
        "Please describe your issue in detail.",
        reply_markup=cancel_keyboard()
    )


async def finish_support_flow(target, context: ContextTypes.DEFAULT_TYPE, user, user_id: int):
    data = user_states[user_id]["data"]

    summary = (
        "🆘 SUPPORT REQUEST RECEIVED\n\n"
        f"Issue type: {data.get('category', '-')}\n"
        f"TOC Username: {data.get('username', '-')}\n"
        f"TOC2.Cloud Email: {data.get('email', '-')}\n"
        f"Details: {data.get('details', '-')}\n\n"
        "⏳ Status: Pending Review\n\n"
        "Your support request has been received and is now under review.\n\n"
        f"If urgent, also contact:\n📧 {SUPPORT_EMAIL}\n📩 {SUPPORT_TELEGRAM}"
    )

    admin_summary = (
        "🆘 NEW SUPPORT REQUEST\n\n"
        f"User ID: {user.id}\n"
        f"Telegram: {safe_username(user)}\n"
        f"Issue type: {data.get('category', '-')}\n"
        f"TOC Username: {data.get('username', '-')}\n"
        f"TOC2.Cloud Email: {data.get('email', '-')}\n"
        f"Details: {data.get('details', '-')}"
    )

    await target.reply_text(summary, reply_markup=main_menu_keyboard())
    await notify_admin_text(context, admin_summary)

    print(f"[SUPPORT FLOW COMPLETE] user={user_id} data={data}")
    clear_user_state(user_id)


async def handle_paid_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
    state = user_states[user_id]
    step = state["step"]

    if step == "username":
        state["data"]["username"] = text
        state["step"] = "email"
        await ask_paid_email(update.message)

    elif step == "email":
        state["data"]["email"] = text
        state["step"] = "screenshot"
        await ask_paid_screenshot(update.message)

    elif step == "extra":
        state["data"]["extra"] = text
        await finish_paid_flow(update.message, context, update.effective_user, user_id)


async def handle_support_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
    state = user_states[user_id]
    step = state["step"]

    if step == "username":
        state["data"]["username"] = text
        state["step"] = "email"
        await ask_support_email(update.message)

    elif step == "email":
        state["data"]["email"] = text
        state["step"] = "details"
        await ask_support_details(update.message)

    elif step == "details":
        state["data"]["details"] = text
        await finish_support_flow(update.message, context, update.effective_user, user_id)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[START] user={user.id} username={user.username}")
    clear_user_state(user.id)
    await send_welcome(update.message)


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = query.data
    print(f"[BUTTON] user={user.id} username={user.username} action={data}")

    if data == "buy":
        clear_user_state(user.id)
        await send_buy(query.message)

    elif data == "crypto":
        clear_user_state(user.id)
        await send_crypto(query.message)

    elif data == "cashapp":
        clear_user_state(user.id)
        await send_cashapp(query.message)

    elif data == "help":
        clear_user_state(user.id)
        await send_support_intro(query.message)

    elif data == "already_paid":
        await start_paid_flow(query.message, user.id)

    elif data == "candidverse":
        clear_user_state(user.id)
        await send_candidverse(query.message)

    elif data == "paid_method_usdt":
        user_states[user.id]["data"]["method"] = "USDT"
        user_states[user.id]["step"] = "username"
        await ask_paid_username(query.message)

    elif data == "paid_method_btc":
        user_states[user.id]["data"]["method"] = "BTC"
        user_states[user.id]["step"] = "username"
        await ask_paid_username(query.message)

    elif data == "paid_method_cashapp":
        user_states[user.id]["data"]["method"] = "CashApp"
        user_states[user.id]["step"] = "username"
        await ask_paid_username(query.message)

    elif data == "support_cat_cloud":
        await start_support_flow(query.message, user.id)
        user_states[user.id]["data"]["category"] = "Cloud activation"
        user_states[user.id]["step"] = "username"
        await ask_support_username(query.message)

    elif data == "support_cat_membership":
        await start_support_flow(query.message, user.id)
        user_states[user.id]["data"]["category"] = "Membership issue"
        user_states[user.id]["step"] = "username"
        await ask_support_username(query.message)

    elif data == "support_cat_payment":
        await start_support_flow(query.message, user.id)
        user_states[user.id]["data"]["category"] = "Payment verification"
        user_states[user.id]["step"] = "username"
        await ask_support_username(query.message)

    elif data == "support_cat_access":
        await start_support_flow(query.message, user.id)
        user_states[user.id]["data"]["category"] = "Access problem"
        user_states[user.id]["step"] = "username"
        await ask_support_username(query.message)

    elif data == "cancel_flow":
        clear_user_state(user.id)
        await query.message.reply_text(
            "❌ Current flow cancelled.",
            reply_markup=main_menu_keyboard()
        )

    elif data == "menu":
        clear_user_state(user.id)
        await send_welcome(query.message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    user_id = user.id

    if user_id in user_states:
        flow = user_states[user_id]["flow"]
        step = user_states[user_id]["step"]

        if flow == "paid" and step == "screenshot":
            if update.message.photo:
                state = user_states[user_id]
                state["data"]["screenshot"] = "photo received"
                photo_file_id = update.message.photo[-1].file_id

                admin_caption = (
                    "📸 PAYMENT SCREENSHOT RECEIVED\n\n"
                    f"User ID: {user.id}\n"
                    f"Telegram: {safe_username(user)}\n"
                    f"Payment method: {state['data'].get('method', '-')}\n"
                    f"TOC Username: {state['data'].get('username', '-')}\n"
                    f"TOC2.Cloud Email: {state['data'].get('email', '-')}"
                )

                await notify_admin_photo(context, photo_file_id, admin_caption)

                state["step"] = "extra"
                await ask_paid_extra(update.message)
                return

    if update.message.text:
        text = update.message.text.lower().strip()
        print(f"[MSG] user={user_id} username={user.username} text={text}")

        if user_id in user_states:
            flow = user_states[user_id]["flow"]

            if flow == "paid":
                await handle_paid_text(update, context, user_id, update.message.text.strip())
                return

            elif flow == "support":
                await handle_support_text(update, context, user_id, update.message.text.strip())
                return

        if contains_any(text, BUY_WORDS):
            await send_buy(update.message)
        elif contains_any(text, CRYPTO_WORDS):
            await send_crypto(update.message)
        elif contains_any(text, CASHAPP_WORDS):
            await send_cashapp(update.message)
        elif contains_any(text, HELP_WORDS):
            await send_support_intro(update.message)
        elif "candidverse" in text or "thecandidverse" in text:
            await send_candidverse(update.message)
        else:
            await send_welcome(update.message)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
