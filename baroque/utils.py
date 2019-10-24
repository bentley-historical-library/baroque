import re


def sanitize_text(text):
    """
    Helper function to remove newlines and extra spaces from a string"""
    if text is None:
        return ""
    else:
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.replace('“', '"').replace('”', '"')
        text = text.strip()
        return text
