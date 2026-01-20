"""
Telegram Bot for searching participants in Google Sheets
Main entry point of the application
"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

# Import configuration and utilities
from config.settings import BOT_TOKEN
from src.utils.logger import setup_logger
from src.bot.states import States, CallbackData
from src.bot.handlers import (
    start_command,
    help_command,
    start_search_callback,
    all_fields_value_entered,
    new_search_callback,
    back_to_menu_callback,
    show_help_callback,
    cancel_callback,
    error_handler,
    ENTERING_ALL_FIELDS_VALUE
)
from src.services.google_sheets import sheets_service

# Initialize logger
setup_logger()
logger = logging.getLogger(__name__)


def main():
    """
    Main function to start the bot
    Initializes handlers and starts polling
    """
    
    logger.info("=" * 50)
    logger.info("Starting Telegram Bot")
    logger.info("=" * 50)
    
    # Test Google Sheets connection on startup
    logger.info("Testing Google Sheets connection...")
    if sheets_service.connect():
        logger.info("✅ Google Sheets connection successful")
        # Pre-fetch data to cache it
        data = sheets_service.get_all_data()
        if data:
            logger.info(f"✅ Successfully loaded {len(data)} records from spreadsheet")
        else:
            logger.warning("⚠️ Connected but no data retrieved")
    else:
        logger.error("❌ Failed to connect to Google Sheets")
        logger.error("Bot will continue but searches will fail until connection is established")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Define conversation handler with states
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_command)
        ],
        states={
            States.MAIN_MENU: [
                CallbackQueryHandler(start_search_callback, pattern=f'^{CallbackData.START_SEARCH}$'),
                CallbackQueryHandler(show_help_callback, pattern=f'^{CallbackData.SHOW_HELP}$'),
            ],
            ENTERING_ALL_FIELDS_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, all_fields_value_entered),
                CallbackQueryHandler(start_search_callback, pattern=f'^{CallbackData.SEARCH_ALL_FIELDS}$'),
                CallbackQueryHandler(cancel_callback, pattern=f'^{CallbackData.CANCEL}$'),
            ],
            States.SHOWING_RESULTS: [
                CallbackQueryHandler(new_search_callback, pattern=f'^{CallbackData.NEW_SEARCH}$'),
                CallbackQueryHandler(back_to_menu_callback, pattern=f'^{CallbackData.BACK_TO_MENU}$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', start_command),
            CallbackQueryHandler(cancel_callback, pattern=f'^{CallbackData.CANCEL}$'),
        ],
        allow_reentry=True
    )
    
    # Add handlers to application
    application.add_handler(conversation_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot is starting polling...")
    logger.info("Press Ctrl+C to stop the bot")
    
    try:
        # Run the bot until interrupted
        application.run_polling(allowed_updates=True)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logger.info("Bot shutdown complete")


if __name__ == '__main__':
    main()
