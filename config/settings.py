"""
Configuration settings for the Telegram bot
Loads environment variables and provides application constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

# Google Sheets Configuration
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1YYvqtrrEG2ssNLbKnsIX3goVQfpeJ-E8wcM06P2ts7Q')
SHEET_NAME = os.getenv('SHEET_NAME', '')  # Empty string means first sheet

# Google credentials file path
GOOGLE_CREDENTIALS_PATH = os.getenv(
    'GOOGLE_CREDENTIALS_PATH',
    str(BASE_DIR / 'config' / 'google_credentials.json')
)

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'logs' / 'bot.log'))

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Column names in the spreadsheet (for reference)
SEARCH_COLUMNS = {
    'surname': 'Фамилия',
    'name': 'Имя',
    'patronymic': 'Отчество',
    'class': 'Класс'
}

RESULT_COLUMNS = {
    'id': 'ID участника',
    'subjects': 'Предметы'
}

# Cache settings (optional, for future optimization)
CACHE_TTL = 300  # Cache time-to-live in seconds (5 minutes)
