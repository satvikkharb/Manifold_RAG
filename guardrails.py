import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BANNED_WORDS = ["kill", "bomb", "attack"]

PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "ssn": r"\b\d{3}-?\d{2}-?\d{4}\b",
    "aadhaar": r"\b\d{4}-?\d{4}-?\d{4}\b"
}

def apply_guardrails(text: str) -> str:
    """Applies guardrails to the input text by checking for banned words and PII patterns."""
    original_text = text
    for word in BANNED_WORDS:
        if word.lower() in text.lower():
            logger.warning(f"Banned word detected: {word}")
            text = text.replace(word, "BANNED_WORD")
    
    for _, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, "[REDACTED]", text)

    if original_text != text:
        logger.info(f"Original Text: {original_text}")
        logger.info(f"Processed Text: {text}")
    else:
        logger.info("No guardrail violations detected.")
    return text