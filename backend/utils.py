def truncate_text(text: str, max_chars: int = 5000) -> str:
    """Truncate text to a maximum number of characters at a sentence boundary.
    If no sentence boundary is found, the text is truncated at max_chars."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    return truncated[:last_period + 1] if last_period != -1 else truncated
