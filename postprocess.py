# post processing
import re
PII_REGEX = re.compile(r'\b(?:\d{3}-\d{2}-\d{4}|\d{3} \d{2} \d{4}|\d{9})\b')  # Simple regex for SSN
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')  # Simple regex for email addresses

def remove_pii(text: str) -> str:
    """Remove personally identifiable information (PII) from the text."""
    return PII_REGEX.sub("[REDACTED]", text)

def remove_emails(text: str) -> str:
    """Remove email addresses from the text."""
    return EMAIL_REGEX.sub("[REDACTED]", text)

def secure_output(text: str) -> str:
    """Apply all post-processing steps to secure the output."""
    text = remove_pii(text)
    text = remove_emails(text)
    return text.strip()
