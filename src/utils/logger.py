"""
Logging configuration for the Telegram bot
Sets up file and console logging with appropriate formatting
"""

import logging
import sys
from pathlib import Path
from config.settings import LOG_LEVEL, LOG_FILE


def setup_logger():
    """
    Configure logging for the application
    Sets up both file and console handlers with formatting
    """
    
    # Create logs directory if it doesn't exist
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )
    
    # File handler - detailed logs
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler - simplified output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    console_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(console_handler)
    
    # Suppress overly verbose third-party loggers
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.INFO)
    
    logging.info("Logging system initialized")
    logging.info(f"Log file: {LOG_FILE}")
    logging.info(f"Log level: {LOG_LEVEL}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Name for the logger (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
