"""
Google Sheets API service
Handles connection to Google Sheets and data retrieval
"""

import logging
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID, SHEET_NAME, SCOPES

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """
    Service for interacting with Google Sheets API
    Reads data from specified spreadsheet
    """
    
    def __init__(self):
        """Initialize Google Sheets service with credentials"""
        self.spreadsheet_id = SPREADSHEET_ID
        self.sheet_name = SHEET_NAME
        self.service = None
        self._data_cache = None
        
    def connect(self) -> bool:
        """
        Establish connection to Google Sheets API
        Returns True if connection successful, False otherwise
        """
        try:
            # Load credentials from service account file
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=SCOPES
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Successfully connected to Google Sheets API")
            return True
            
        except FileNotFoundError:
            logger.error(f"Credentials file not found: {GOOGLE_CREDENTIALS_PATH}")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Google Sheets API: {e}")
            return False
    
    def get_all_data(self, force_refresh: bool = False) -> Optional[List[Dict[str, str]]]:
        """
        Retrieve all data from the spreadsheet
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of dictionaries where keys are column names and values are cell values
            Returns None if error occurs
        """
        # Return cached data if available and not forcing refresh
        if self._data_cache and not force_refresh:
            logger.info("Returning cached data")
            return self._data_cache
        
        # Ensure service is connected
        if not self.service:
            if not self.connect():
                return None
        
        try:
            # Determine the range to read
            range_name = f"{self.sheet_name}!A:Z" if self.sheet_name else "A:Z"
            
            # Call the Sheets API
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No data found in spreadsheet")
                return []
            
            # First row contains headers
            headers = values[0]
            data = []
            
            # Convert rows to dictionaries
            for row in values[1:]:
                # Handle rows with missing cells (pad with empty strings)
                row_data = row + [''] * (len(headers) - len(row))
                row_dict = {headers[i]: row_data[i] for i in range(len(headers))}
                data.append(row_dict)
            
            # Cache the data
            self._data_cache = data
            logger.info(f"Successfully retrieved {len(data)} rows from spreadsheet")
            return data
            
        except HttpError as e:
            logger.error(f"HTTP error while fetching data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching data: {e}")
            return None
    
    def get_headers(self) -> Optional[List[str]]:
        """
        Get column headers from the spreadsheet
        
        Returns:
            List of column names or None if error occurs
        """
        if not self.service:
            if not self.connect():
                return None
        
        try:
            range_name = f"{self.sheet_name}!A1:Z1" if self.sheet_name else "A1:Z1"
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            headers = result.get('values', [[]])[0]
            logger.info(f"Retrieved {len(headers)} column headers")
            return headers
            
        except Exception as e:
            logger.error(f"Error fetching headers: {e}")
            return None
    
    def clear_cache(self):
        """Clear cached data to force fresh retrieval on next request"""
        self._data_cache = None
        logger.info("Data cache cleared")


# Create a singleton instance
sheets_service = GoogleSheetsService()
