     """
Solana CA Forwarder Bot
-----------------------
Watches messages in one or more source chats, detects Solana contract
(token mint) addresses, and forwards them to a target group/channel
prefixed with "/soc".

Environment variables (see .env.example):
    BOT_TOKEN         - Telegram bot token from @BotFather
    TARGET_CHAT_ID    - Chat ID the "/soc <address>" messages are sent to
    SOURCE_CHAT_IDS    - Optional comma-separated whitelist of chat IDs to
                          watch. If empty, the bot watches every chat/group
                          it has been added to.
    INCLUDE_SOURCE_INFO - "true"/"false" (default "true"). If true, a short
                          line with the source chat/user is appended.
"""

import base58
import logging
import os
import re
from typing import Iterable, Set

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("solana-ca-forwarder")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_CHAT_ID = os.environ.get("TARGET_CHAT_ID")
SOURCE_CHAT_IDS_RAW = os.environ.get("SOURCE_CHAT_IDS", "").strip()
INCLUDE_SOURCE_INFO = os.environ.get("INCLUDE_SOURCE_INFO", "true").lower() == "true"

SOURCE_CHAT_IDS: Set[int] = set()
if SOURCE_CHAT_IDS_RAW:
    for chunk in SOURCE_CHAT_IDS_RAW.split(","):
        chunk = chunk.strip()
        if chunk:
            SOURCE_CHAT_IDS.add(int(chunk))

# Rough candidate pattern first (cheap pre-filter): base58 alphabet,
# 32-44 chars long. We then verify it actually decodes to a 32-byte
# public key, which is what filters out almost all false positives
# (random words, hashes, tx signatures that are the wrong length, etc).
CANDIDATE_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")


def find_solana_addresses(text: str) -> Iterable[str]:
    """Return the set of valid Solana addresses found in `text`, in the
    order they first appear, without duplicates."""
    if not text:
        return []

    seen: Set[str] = set()
    ordered = []
    for candidate in CANDIDATE_RE.findall(text):
        if candidate in seen:
            continue
        try:
            decoded = base58.b58decode(candidate)
        except Exception:
            continue
        # Solana public keys (token mints, wallets, program IDs) are
        # always exactly 32 raw bytes.
        if len(decoded) == 32:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Solana CA Forwarder is running.\n"
        "Add me to a group, give me permission to read messages, and any "
        "Solana contract address posted there will be forwarded to the "
        "configured target chat as `/soc <address>`.\n\n"
        "Use /id in any chat to get its chat ID for configuration.",
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: `{chat.id}`", parse_mode=ParseMode.MARKDOWN)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    chat = update.effective_chat
    if message is None or chat is None:
        return

    # If a whitelist is configured, ignore chats not on it.
    if SOURCE_CHAT_IDS and chat.id not in SOURCE_CHAT_IDS:
        return

    text = message.text or message.caption
    if not text:
        return

    addresses = find_solana_addresses(text)
    if not addresses:
        return

    if not TARGET_CHAT_ID:
        logger.warning("Detected %s but TARGET_CHAT_ID is not set", addresses)
        return

    sender = update.effective_user
    sender_name = sender.full_name if sender else "Unknown"
    sender_username = f"@{sender.username}" if sender and sender.username else ""

    for address in addresses:
        outgoing = f"/soc {address}"
        if INCLUDE_SOURCE_INFO:
            source_line = f"\n\nFrom: {chat.title or chat.id} • {sender_name} {sender_username}".rstrip()
            outgoing += source_line

        try:
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=outgoing)
            logger.info("Forwarded %s from chat %s to %s", address, chat.id, TARGET_CHAT_ID)
        except Exception as exc:
            logger.exception("Failed to forward %s: %s", address, exc)


def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN environment variable is required.")
    if not TARGET_CHAT_ID:
        logger.warning(
            "TARGET_CHAT_ID is not set. The bot will detect addresses but "
            "will not be able to forward them until it is configured."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(
        MessageHandler(filters.TEXT | filters.CAPTION, handle_message)
    )

    logger.info("Bot starting (polling mode)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()   
        
