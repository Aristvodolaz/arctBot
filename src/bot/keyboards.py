"""
Inline keyboard layouts for the Telegram bot
Creates interactive buttons for user navigation
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.bot.states import CallbackData


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Main menu keyboard with start search button
    
    Returns:
        InlineKeyboardMarkup for the main menu
    """
    keyboard = [
        [InlineKeyboardButton("🔍 Начать поиск", callback_data=CallbackData.START_SEARCH)],
        [InlineKeyboardButton("ℹ️ Справка", callback_data=CallbackData.SHOW_HELP)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_field_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard for search - only combined search by all fields
    
    Returns:
        InlineKeyboardMarkup for field selection
    """
    keyboard = [
        [InlineKeyboardButton("🔍 Начать поиск", callback_data=CallbackData.SEARCH_ALL_FIELDS)],
        [InlineKeyboardButton("❌ Отмена", callback_data=CallbackData.CANCEL)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_new_search_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard shown after displaying search results
    Allows user to start a new search or return to main menu
    
    Returns:
        InlineKeyboardMarkup for post-results actions
    """
    keyboard = [
        [InlineKeyboardButton("🔍 Новый поиск", callback_data=CallbackData.NEW_SEARCH)],
        [InlineKeyboardButton("🏠 Главное меню", callback_data=CallbackData.BACK_TO_MENU)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Simple keyboard with cancel button
    Used during text input steps
    
    Returns:
        InlineKeyboardMarkup with cancel button
    """
    keyboard = [
        [InlineKeyboardButton("❌ Отмена", callback_data=CallbackData.CANCEL)]
    ]
    return InlineKeyboardMarkup(keyboard)
