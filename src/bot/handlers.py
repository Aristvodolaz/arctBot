"""
Telegram bot handlers
Handles commands, callbacks, and user messages
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.bot.states import States, CallbackData
from src.bot.keyboards import (
    get_main_menu_keyboard,
    get_field_selection_keyboard,
    get_new_search_keyboard,
    get_cancel_keyboard
)
from src.services.google_sheets import sheets_service
from src.services.search import search_service
from config.settings import SEARCH_COLUMNS

# State for combined search
ENTERING_ALL_FIELDS_VALUE = 10  # New state for entering combined search data

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for /start command
    Shows welcome message and main menu
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_text = (
        f"👋 Здравствуйте, {user.first_name}!\n\n"
        "Я помогу вам найти информацию об участниках.\n\n"
        "Вы можете искать по:\n"
        "• Фамилии\n"
        "• Имени\n"
        "• Отчеству\n"
        "• Классу\n\n"
        "Нажмите кнопку ниже, чтобы начать поиск."
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
    
    return States.MAIN_MENU


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /help command
    Shows help information
    """
    help_text = (
        "ℹ️ <b>Справка по использованию бота</b>\n\n"
        "<b>Команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n\n"
        "<b>Как использовать:</b>\n"
        "1. Нажмите 'Начать поиск'\n"
        "2. Выберите поле для поиска (Фамилия/Имя/Отчество/Класс)\n"
        "3. Введите значение для поиска\n"
        "4. Получите результаты\n\n"
        "<b>Особенности поиска:</b>\n"
        "• Поиск НЕ учитывает регистр (ИВАНОВ = иванов)\n"
        "• Поиск ищет ТОЧНОЕ совпадение\n"
        "• Если найдено несколько результатов, будут показаны все\n\n"
        "<b>Что вы получите:</b>\n"
        "• ID участника\n"
        "• Список предметов участника"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='HTML'
    )


async def start_search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for 'Start Search' button
    Asks user to enter all data at once
    """
    query = update.callback_query
    await query.answer()
    
    logger.info(f"User {query.from_user.id} started search")
    
    # Mark that we're doing combined search
    context.user_data['search_mode'] = 'all_fields'
    
    await query.edit_message_text(
        "✍️ <b>Введите данные для поиска:</b>\n\n"
        "Формат: Фамилия Имя Отчество Класс\n\n"
        "Например: <code>Иванов Иван Иванович 10</code>",
        parse_mode='HTML',
        reply_markup=get_cancel_keyboard()
    )
    
    return ENTERING_ALL_FIELDS_VALUE


async def all_fields_value_entered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for user input when searching by all fields
    Parses input and performs combined search
    """
    user = update.effective_user
    search_text = update.message.text.strip()
    
    if not search_text:
        await update.message.reply_text(
            "❌ Вы не ввели данные. Попробуйте снова:\n\n"
            "Формат: Фамилия Имя Отчество Класс",
            reply_markup=get_cancel_keyboard()
        )
        return ENTERING_ALL_FIELDS_VALUE
    
    # Parse input - split by spaces
    parts = search_text.split()
    
    if len(parts) < 4:
        await update.message.reply_text(
            "❌ Недостаточно данных. Введите все 4 параметра:\n\n"
            "Формат: Фамилия Имя Отчество Класс\n"
            "Например: <code>Иванов Иван Иванович 10</code>",
            parse_mode='HTML',
            reply_markup=get_cancel_keyboard()
        )
        return ENTERING_ALL_FIELDS_VALUE
    
    # Extract fields
    surname = parts[0]
    name = parts[1]
    patronymic = parts[2]
    class_name = ' '.join(parts[3:])  # In case class has spaces
    
    logger.info(f"User {user.id} searching by all fields: {surname} {name} {patronymic} {class_name}")
    
    # Show "searching" message
    status_message = await update.message.reply_text("🔄 Ищу...")
    
    try:
        # Fetch data from Google Sheets
        data = sheets_service.get_all_data()
        
        if data is None:
            await status_message.edit_text(
                "❌ Ошибка подключения к Google Sheets.\n"
                "Пожалуйста, попробуйте позже.",
                reply_markup=get_main_menu_keyboard()
            )
            return States.MAIN_MENU
        
        # Perform combined search
        results = search_service.search_by_all_fields(
            data, surname, name, patronymic, class_name
        )
        
        # Format and send results
        formatted_results = search_service.format_results(results)
        
        await status_message.edit_text(
            formatted_results,
            reply_markup=get_new_search_keyboard()
        )
        
        logger.info(f"Combined search completed for user {user.id}: {len(results)} results found")
        
    except Exception as e:
        logger.error(f"Error during combined search: {e}", exc_info=True)
        await status_message.edit_text(
            "❌ Произошла ошибка при поиске. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard()
        )
    
    # Clear search mode
    context.user_data.pop('search_mode', None)
    
    return States.SHOWING_RESULTS


async def new_search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for 'New Search' button
    Asks user to enter new search data
    """
    query = update.callback_query
    await query.answer()
    
    logger.info(f"User {query.from_user.id} starting new search")
    
    # Clear previous search data
    context.user_data.clear()
    context.user_data['search_mode'] = 'all_fields'
    
    await query.edit_message_text(
        "✍️ <b>Введите данные для поиска:</b>\n\n"
        "Формат: Фамилия Имя Отчество Класс\n\n"
        "Например: <code>Иванов Иван Иванович 10А</code>",
        parse_mode='HTML',
        reply_markup=get_cancel_keyboard()
    )
    
    return ENTERING_ALL_FIELDS_VALUE


async def back_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for 'Back to Menu' button
    Returns to main menu
    """
    query = update.callback_query
    await query.answer()
    
    logger.info(f"User {query.from_user.id} returned to main menu")
    
    # Clear search data
    context.user_data.clear()
    
    await query.edit_message_text(
        "🏠 Главное меню\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    
    return States.MAIN_MENU


async def show_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for 'Help' button from main menu
    Shows help information
    """
    query = update.callback_query
    await query.answer()
    
    help_text = (
        "ℹ️ <b>Справка по использованию бота</b>\n\n"
        "<b>Как использовать:</b>\n"
        "1. Нажмите 'Начать поиск'\n"
        "2. Выберите поле для поиска\n"
        "3. Введите значение\n"
        "4. Получите результаты\n\n"
        "<b>Особенности:</b>\n"
        "• Регистр НЕ важен\n"
        "• Точное совпадение\n"
        "• Показываются все результаты"
    )
    
    await query.edit_message_text(
        help_text,
        parse_mode='HTML',
        reply_markup=get_main_menu_keyboard()
    )
    
    return States.MAIN_MENU


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for 'Cancel' button
    Returns to main menu and clears user data
    """
    query = update.callback_query
    await query.answer("Поиск отменён")
    
    logger.info(f"User {query.from_user.id} cancelled operation")
    
    # Clear user data
    context.user_data.clear()
    
    await query.edit_message_text(
        "❌ Операция отменена.\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    
    return States.MAIN_MENU


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler for the bot
    Logs errors and notifies user
    """
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка. Пожалуйста, попробуйте позже или используйте /start"
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")
