"""
Search service for finding participants in spreadsheet data
Implements case-insensitive exact match search
"""

import logging
from typing import List, Dict, Optional
from config.settings import SEARCH_COLUMNS, RESULT_COLUMNS

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for searching participants in spreadsheet data
    Supports search by surname, name, patronymic, or class
    """
    
    @staticmethod
    def search_by_field(
        data: List[Dict[str, str]],
        field_name: str,
        search_value: str
    ) -> List[Dict[str, str]]:
        """
        Search for participants by a specific field
        
        Args:
            data: List of participant records from spreadsheet
            field_name: Name of the field to search (e.g., 'Фамилия', 'Имя')
            search_value: Value to search for (case-insensitive exact match)
            
        Returns:
            List of matching records
        """
        if not data:
            logger.warning("Search called with empty data")
            return []
        
        if not search_value:
            logger.warning("Search called with empty search value")
            return []
        
        # Normalize search value (case-insensitive)
        search_value_lower = search_value.strip().lower()
        
        results = []
        for record in data:
            # Get field value from record
            field_value = record.get(field_name, '').strip().lower()
            
            # Exact match (case-insensitive)
            if field_value == search_value_lower:
                results.append(record)
        
        logger.info(f"Search by '{field_name}' for '{search_value}' found {len(results)} results")
        return results
    
    @staticmethod
    def search_by_all_fields(
        data: List[Dict[str, str]],
        surname: str,
        name: str,
        patronymic: str,
        class_name: str
    ) -> List[Dict[str, str]]:
        """
        Search for participants by all fields at once
        
        Args:
            data: List of participant records from spreadsheet
            surname: Surname to search for
            name: Name to search for
            patronymic: Patronymic to search for
            class_name: Class to search for
            
        Returns:
            List of matching records (all fields must match)
        """
        if not data:
            logger.warning("Search called with empty data")
            return []
        
        # Normalize all search values (case-insensitive)
        surname_lower = surname.strip().lower()
        name_lower = name.strip().lower()
        patronymic_lower = patronymic.strip().lower()
        class_lower = class_name.strip().lower()
        
        results = []
        for record in data:
            # Get field values from record
            record_surname = record.get(SEARCH_COLUMNS['surname'], '').strip().lower()
            record_name = record.get(SEARCH_COLUMNS['name'], '').strip().lower()
            record_patronymic = record.get(SEARCH_COLUMNS['patronymic'], '').strip().lower()
            record_class = record.get(SEARCH_COLUMNS['class'], '').strip().lower()
            
            # All fields must match (exact match, case-insensitive)
            if (record_surname == surname_lower and
                record_name == name_lower and
                record_patronymic == patronymic_lower and
                record_class == class_lower):
                results.append(record)
        
        logger.info(f"Search by all fields for '{surname} {name} {patronymic} {class_name}' found {len(results)} results")
        return results
    
    @staticmethod
    def format_results(results: List[Dict[str, str]]) -> str:
        """
        Format search results for display in Telegram
        
        Args:
            results: List of matching records
            
        Returns:
            Formatted string for Telegram message
        """
        if not results:
            return "❌ Ничего не найдено. Попробуйте изменить параметры поиска."
        
        # Build formatted message
        message_parts = [f"✅ Найдено результатов: {len(results)}\n"]
        
        for idx, record in enumerate(results, 1):
            message_parts.append(f"━━━━━━━━━━━━━━━━━━━━")
            message_parts.append(f"📋 Результат #{idx}")
            message_parts.append("")
            
            # Add search fields for context
            surname = record.get(SEARCH_COLUMNS['surname'], 'N/A')
            name = record.get(SEARCH_COLUMNS['name'], 'N/A')
            patronymic = record.get(SEARCH_COLUMNS['patronymic'], 'N/A')
            class_name = record.get(SEARCH_COLUMNS['class'], 'N/A')
            
            message_parts.append(f"👤 ФИО: {surname} {name} {patronymic}")
            message_parts.append(f"🏫 Класс: {class_name}")
            message_parts.append("")
            
            # Add result fields (ID and Subjects)
            participant_id = record.get(RESULT_COLUMNS['id'], 'N/A')
            subjects = record.get(RESULT_COLUMNS['subjects'], 'N/A')
            
            message_parts.append(f"🆔 ID участника: {participant_id}")
            message_parts.append(f"📚 Предметы:")
            
            # Format subjects (handle multiline text)
            if subjects and subjects != 'N/A':
                # Split by newlines if present
                subject_lines = subjects.split('\n')
                for subject_line in subject_lines:
                    subject_line = subject_line.strip()
                    if subject_line:
                        message_parts.append(f"   • {subject_line}")
            else:
                message_parts.append("   • Не указаны")
            
            message_parts.append("")
        
        return "\n".join(message_parts)
    
    @staticmethod
    def validate_field_name(field_name: str) -> bool:
        """
        Validate if field name is one of the searchable columns
        
        Args:
            field_name: Name of the field to validate
            
        Returns:
            True if field name is valid, False otherwise
        """
        valid_fields = list(SEARCH_COLUMNS.values())
        return field_name in valid_fields
    
    @staticmethod
    def get_field_display_name(field_key: str) -> Optional[str]:
        """
        Get display name for a field key
        
        Args:
            field_key: Key from SEARCH_COLUMNS (e.g., 'surname', 'name')
            
        Returns:
            Display name (e.g., 'Фамилия', 'Имя') or None if not found
        """
        return SEARCH_COLUMNS.get(field_key)


# Create a singleton instance
search_service = SearchService()
