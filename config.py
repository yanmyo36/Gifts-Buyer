import configparser
from pathlib import Path

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# =======================
# GENERAL CONFIGURATION
# =======================
SESSION: str = str(Path(__file__).parent / "data/account")
API_ID: int = config.getint('Telegram', 'API_ID')
API_HASH: str = config.get('Telegram', 'API_HASH')
PHONE_NUMBER: str = config.get('Telegram', 'PHONE_NUMBER')
DATA_FILEPATH: Path = Path(__file__).parent / "data/json/history.json"

# =========================
# BOT SETTINGS
# =========================
INTERVAL: float = config.getfloat('Bot', 'INTERVAL')
TIMEZONE: str = config.get('Bot', 'TIMEZONE')
CHANNEL_ID: int = config.getint('Telegram', 'CHANNEL_ID')

# =========================
# GIFTS | USER INFO
# =========================
USER_ID = []
user_ids = config.get('Gifts', 'USER_ID').split(',')

for user_id in user_ids:
    try:
        USER_ID.append(int(user_id))
    except ValueError:
        USER_ID.append(user_id)

MAX_GIFT_PRICE: int = config.getint('Gifts', 'MAX_GIFT_PRICE')
GIFT_DELAY: float = config.getfloat('Gifts', 'GIFT_DELAY')

PURCHASE_NON_LIMITED_GIFTS: bool = config.getboolean('Gifts', 'PURCHASE_NON_LIMITED_GIFTS')
HIDE_SENDER_NAME: bool = config.getboolean('Gifts', 'HIDE_SENDER_NAME')
GIFT_IDS: list[int] = [int(gift_id) for gift_id in config.get('Gifts', 'GIFT_IDS').split(",") if gift_id]

# Parse gift ranges from config
GIFT_RANGES = []
for range_str, quantity in config.items('Ranges'):
    try:
        min_price, max_price, supply_limit = map(int, range_str.split(','))
        GIFT_RANGES.append((min_price, max_price, supply_limit, int(quantity)))
    except (ValueError, AttributeError):
        continue


def get_num_gifts(gift_price: float) -> int:
    """
    Determine number of gifts to send based on gift price and supply limits.
    
    Args:
        gift_price: Price of the gift
        
    Returns:
        int: Number of gifts to send
    """
    for min_price, max_price, supply_limit, num_gifts in GIFT_RANGES:
        if min_price <= gift_price < max_price:
            return min(num_gifts, supply_limit)
    return 1  # Default to 1 gift if no range matches


# =========================
# LOCALE SETTINGS
# =========================
LANGUAGE: str = config.get('Bot', 'LANGUAGE').upper()
LANG_CODES = {
    "EN": "locales.en",
    "RU": "locales.ru",
    "UK": "locales.uk",
}

locale = __import__(LANG_CODES.get(LANGUAGE, "locales.en"), fromlist=[""])
