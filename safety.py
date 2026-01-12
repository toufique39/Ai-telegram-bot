BANNED_TOPICS = [
    "হ্যাক",
    "illegal",
    "credit card",
    "password",
    "otp"
]

def is_safe(text: str) -> bool:
    if not text:
        return True
    text = text.lower()
    for word in BANNED_TOPICS:
        if word in text:
            return False
    return True
