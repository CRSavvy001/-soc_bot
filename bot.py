
import os
import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Solana address pattern (base58, typically 32-44 characters)
SOLANA_ADDRESS_PATTERN = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
SOURCE_CHAT_ID = os.getenv('SOURCE_CHAT_ID')  # The group/channel to monitor
DESTINATION_CHAT_ID = os.getenv('DESTINATION_CHAT_ID')  # Where to send modified messages

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and detect Solana addresses"""
    
    # Only process messages from the source chat
    if str(update.effective_chat.id) != SOURCE_CHAT_ID:
        return
    
    message_text = update.message.text or update.message.caption or ""
    
    # Find all Solana addresses in the message
    solana_addresses = re.findall(SOLANA_ADDRESS_PATTERN, message_text)
    
    if solana_addresses:
        logger.info(f"Found {len(solana_addresses)} Solana address(es) in message")
        
        # Process each address
        for address in solana_addresses:
            # Add /nar before the address
            modified_address = f"/soc {address}"
            
            try:
                # Send to destination chat
                await context.bot.send_message(
                    chat_id=DESTINATION_CHAT_ID,
                    text=modified_address
                )
                logger.info(f"Sent modified address to destination: {modified_address}")
            except Exception as e:
                logger.error(f"Error sending message: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    
    # Validate environment variables
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables")
        return
    
    if not SOURCE_CHAT_ID:
        logger.error("SOURCE_CHAT_ID not found in environment variables")
        return
    
    if not DESTINATION_CHAT_ID:
        logger.error("DESTINATION_CHAT_ID not found in environment variables")
        return
    
    logger.info("Starting Solana Address Forwarder Bot...")
    logger.info(f"Monitoring chat: {SOURCE_CHAT_ID}")
    logger.info(f"Forwarding to: {DESTINATION_CHAT_ID}")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add message handler
    application.add_handler(MessageHandler(
        filters.TEXT | filters.CAPTION,
        handle_message
    ))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
              
