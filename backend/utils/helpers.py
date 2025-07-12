from datetime import datetime
import re
from typing import Optional

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    Supports international format with country code
    """
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))

def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard format
    """
    # Remove any spaces, dashes, or parentheses
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Add + if not present and number doesn't start with 0
    if not cleaned.startswith('+') and not cleaned.startswith('0'):
        cleaned = '+' + cleaned
    
    return cleaned

def get_current_timestamp() -> datetime:
    """
    Get current UTC timestamp
    """
    return datetime.utcnow()

def validate_skill(skill: str) -> bool:
    """
    Validate skill name
    """
    common_skills = [
        'mason', 'carpenter', 'plumber', 'electrician', 'painter',
        'welder', 'driver', 'helper', 'gardener', 'cleaner',
        'cook', 'security', 'mechanic', 'tailor', 'barber'
    ]
    return skill.lower() in common_skills

def validate_language(language: str) -> bool:
    """
    Validate language
    """
    common_languages = [
        'hindi', 'english', 'bengali', 'marathi', 'tamil',
        'telugu', 'gujarati', 'kannada', 'malayalam', 'punjabi',
        'oriya', 'assamese', 'urdu'
    ]
    return language.lower() in common_languages

def sanitize_string(input_str: str) -> str:
    """
    Sanitize string input by removing extra spaces and converting to title case
    """
    return input_str.strip().title()