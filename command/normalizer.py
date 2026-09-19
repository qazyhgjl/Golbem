"""
Persian text normalizer converting digits, removing diacritics and extra punctuation.
"""

import re

# Digit maps
PERSIAN_ARABIC_DIGITS = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
}

PERSIAN_WORD_NUMBERS = {
    'یک': 1, 'دو': 2, 'سه': 3, 'چهار': 4, 'پنج': 5,
    'شش': 6, 'شیش': 6, 'هفت': 7, 'هشت': 8, 'نه': 9, 'ده': 10,
    'یازده': 11, 'دوازده': 12, 'سیزده': 13, 'چهارده': 14, 'پانزده': 15,
    'شانزده': 16, 'هفده': 17, 'هجده': 18, 'نوزده': 19, 'بیست': 20,
    'سی': 30, 'چهل': 40, 'پنجاه': 50, 'شصت': 60,
}

def convert_digits(text: str) -> str:
    """Converts Persian and Arabic digits to ASCII digits."""
    for p_digit, e_digit in PERSIAN_ARABIC_DIGITS.items():
        text = text.replace(p_digit, e_digit)
    return text

def normalize_text(text: str) -> str:
    """Normalizes Persian text for command interpretation."""
    if not text:
        return ""

    # Convert digits
    text = convert_digits(text)

    # Convert Arabic characters
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('ة', 'ه')

    # Remove Arabic diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

    # Standardize half-spaces and multi-spaces
    text = text.replace('\u200c', ' ')
    text = re.sub(r'\s+', ' ', text).strip()

    return text
