import random
import string


def generate_short_code(length: int = 7) -> str:
    chars = string.digits + string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))
