import string
import secrets

def generate_short_id(size: int = 8) -> str:
    """
    Генерирует криптографически безопасный случайный идентификатор.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(size))
