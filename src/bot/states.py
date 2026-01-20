"""
FSM (Finite State Machine) states for the Telegram bot
Defines conversation states for step-by-step user interaction
"""

from telegram.ext import ConversationHandler


# Conversation states
class States:
    """
    States for the conversation flow
    Used with ConversationHandler to manage multi-step interactions
    """
    
    # Main menu state
    MAIN_MENU = 0
    
    # Search flow states
    SELECTING_FIELD = 1  # User is selecting which field to search by
    ENTERING_VALUE = 2   # User is entering the search value
    SHOWING_RESULTS = 3  # Displaying search results
    
    # End conversation
    END = ConversationHandler.END


# Callback data for inline keyboard buttons
class CallbackData:
    """
    Callback data identifiers for inline keyboard buttons
    """
    
    # Main menu actions
    START_SEARCH = "start_search"
    SHOW_HELP = "show_help"
    
    # Field selection
    SEARCH_ALL_FIELDS = "search_all_fields"  # Search by all fields at once
    
    # Action buttons
    NEW_SEARCH = "new_search"
    CANCEL = "cancel"
    BACK_TO_MENU = "back_to_menu"
