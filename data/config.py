import configparser
import sys
from pathlib import Path
from typing import List, Union, Dict

from app.utils.localization import localization
from app.utils.logger import error


class Config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self._load_config()
        self._setup_paths()
        self._setup_properties()
        self._validate()
        localization.set_locale(self.LANGUAGE)

    def _load_config(self) -> None:
        config_file = Path('config.ini')
        if not config_file.exists():
            error("Configuration file 'config.ini' not found!")
            sys.exit(1)
        self.parser.read(config_file, encoding='utf-8')

    def _setup_paths(self) -> None:
        base_dir = Path(__file__).parent
        self.SESSION = str(base_dir.parent / "data/account")
        self.DATA_FILEPATH = base_dir / "json/history.json"

    def _setup_properties(self) -> None:
        self.API_ID = self.parser.getint('Telegram', 'API_ID', fallback=0)
        self.API_HASH = self.parser.get('Telegram', 'API_HASH', fallback='')
        self.PHONE_NUMBER = self.parser.get('Telegram', 'PHONE_NUMBER', fallback='')
        self.CHANNEL_ID = self.parser.getint('Telegram', 'CHANNEL_ID', fallback=0) or None

        self.INTERVAL = self.parser.getfloat('Bot', 'INTERVAL', fallback=15.0)
        self.LANGUAGE = self.parser.get('Bot', 'LANGUAGE', fallback='EN').lower()

        self.USER_ID = self._parse_recipients()
        self.PRICE_RANGES = self._parse_price_ranges()
        self.GIFT_QUANTITY = self.parser.getint('Gifts', 'GIFT_QUANTITY', fallback=1)
        self.PURCHASE_NON_LIMITED_GIFTS = self.parser.getboolean('Gifts', 'PURCHASE_NON_LIMITED_GIFTS', fallback=False)
        self.PURCHASE_ONLY_UPGRADABLE_GIFTS = self.parser.getboolean('Gifts', 'PURCHASE_ONLY_UPGRADABLE_GIFTS',
                                                                     fallback=False)

    def _parse_recipients(self) -> List[Union[int, str]]:
        raw_ids = self.parser.get('Gifts', 'USER_ID', fallback='').split(',')
        recipients = []
        for user_id in raw_ids:
            user_id = user_id.strip()
            if user_id:
                try:
                    recipients.append(int(user_id))
                except ValueError:
                    recipients.append(user_id)
        return recipients

    def _parse_price_ranges(self) -> List[Dict[str, int]]:
        ranges_str = self.parser.get('Gifts', 'PRICE_RANGES', fallback='')
        ranges = []

        for range_item in ranges_str.split(','):
            range_item = range_item.strip()
            if not range_item:
                continue

            try:
                price_part, supply_part = range_item.split(':')
                min_price, max_price = map(int, price_part.strip().split('-'))
                supply_limit = int(supply_part.strip())

                ranges.append({
                    'min_price': min_price,
                    'max_price': max_price,
                    'supply_limit': supply_limit
                })
            except (ValueError, IndexError):
                error(f"Invalid price range format: {range_item}")
                continue

        return ranges

    def get_matching_range(self, price: int, total_amount: int) -> bool:
        for range_config in self.PRICE_RANGES:
            if (range_config['min_price'] <= price <= range_config['max_price'] and
                    total_amount <= range_config['supply_limit']):
                return True
        return False

    def _validate(self) -> None:
        checks = {
            "Telegram > API_ID": self.API_ID == 0,
            "Telegram > API_HASH": not self.API_HASH,
            "Telegram > PHONE_NUMBER": not self.PHONE_NUMBER,
            "Gifts > USER_ID": not self.USER_ID,
            "Gifts > PRICE_RANGES": not self.PRICE_RANGES,
            "Gifts > GIFT_QUANTITY (> 0)": self.GIFT_QUANTITY <= 0,
        }

        invalid = [field for field, invalid in checks.items() if invalid]
        if invalid:
            error_msg = localization.translate("errors.missing_config").format(
                '\n'.join(f'- {field}' for field in invalid))
            error(error_msg)
            sys.exit(1)

    @property
    def language_display(self) -> str:
        return localization.get_display_name(self.LANGUAGE)

    @property
    def language_code(self) -> str:
        return localization.get_language_code(self.LANGUAGE)


config = Config()
t = localization.translate
get_language_display = localization.get_display_name
get_language_code = localization.get_language_code
get_all_translations = localization.load_all_translations
