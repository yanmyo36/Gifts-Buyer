import configparser
import sys
from importlib import import_module
from pathlib import Path
from typing import List, Tuple

from utils.logger import error


class Config:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config.ini')
        self._init_paths()
        self._init_telegram_settings()
        self._init_bot_settings()
        self._init_gift_settings()
        self._init_locale()
        self._validate_config()

    def _init_paths(self):
        self.SESSION = str(Path(__file__).parent.parent / "data/account")
        self.DATA_FILEPATH = Path(__file__).parent / "json/history.json"

    def _init_telegram_settings(self):
        self.API_ID = self.config_parser.getint('Telegram', 'API_ID', fallback=0)
        self.API_HASH = self.config_parser.get('Telegram', 'API_HASH', fallback='')
        self.PHONE_NUMBER = self.config_parser.get('Telegram', 'PHONE_NUMBER', fallback='')
        self.CHANNEL_ID = self.config_parser.getint('Telegram', 'CHANNEL_ID', fallback=0)

    def _init_bot_settings(self):
        self.INTERVAL = self.config_parser.getfloat('Bot', 'INTERVAL', fallback=10.0)
        self.TIMEZONE = self.config_parser.get('Bot', 'TIMEZONE', fallback='UTC')
        self.LANGUAGE = self.config_parser.get('Bot', 'LANGUAGE', fallback='EN').upper()

    def _init_gift_settings(self):
        self.USER_ID = self._parse_user_ids()
        self.MAX_GIFT_PRICE = self.config_parser.getint('Gifts', 'MAX_GIFT_PRICE', fallback=10000)
        self.GIFT_DELAY = self.config_parser.getfloat('Gifts', 'GIFT_DELAY', fallback=5.0)
        self.PURCHASE_NON_LIMITED_GIFTS = self.config_parser.getboolean('Gifts', 'PURCHASE_NON_LIMITED_GIFTS',
                                                                        fallback=False)
        self.HIDE_SENDER_NAME = self.config_parser.getboolean('Gifts', 'HIDE_SENDER_NAME', fallback=True)
        self.GIFT_IDS = self._parse_gift_ids()
        self.GIFT_RANGES = self._parse_gift_ranges()

    def _parse_user_ids(self) -> List:
        user_ids = []
        for user_id in self.config_parser.get('Gifts', 'USER_ID', fallback='').split(','):
            user_id = user_id.strip()
            if user_id:
                try:
                    user_ids.append(int(user_id))
                except ValueError:
                    user_ids.append(user_id)
        return user_ids

    def _parse_gift_ids(self) -> List[int]:
        return [
            int(gift_id) for gift_id in self.config_parser.get('Gifts', 'GIFT_IDS', fallback='').split(',')
            if gift_id.strip()
        ]

    def _parse_gift_ranges(self) -> List[Tuple[int, int, int, int]]:
        ranges = []
        if self.config_parser.has_section('Ranges'):
            for range_str, quantity in self.config_parser.items('Ranges'):
                try:
                    min_price, max_price, supply_limit = map(int, range_str.split(','))
                    ranges.append((min_price, max_price, supply_limit, int(quantity)))
                except (ValueError, AttributeError):
                    continue
        return ranges

    def _init_locale(self):
        lang_codes = {
            "EN": "locales.en",
            "RU": "locales.ru",
            "UK": "locales.uk",
        }

        try:
            self.locale = import_module(lang_codes.get(self.LANGUAGE, "locales.en"))
        except ModuleNotFoundError:
            self.locale = import_module("locales.en")
            self.LANGUAGE = "EN"

    def get_num_gifts(self, gift_price: float) -> int:
        for min_price, max_price, _, num_gifts in self.GIFT_RANGES:
            if min_price <= gift_price < max_price:
                return num_gifts
        return 1

    def _validate_config(self):
        missing_fields = []

        if self.API_ID == 0:
            missing_fields.append("Telegram > API_ID")
        if not self.API_HASH:
            missing_fields.append("Telegram > API_HASH")
        if not self.PHONE_NUMBER:
            missing_fields.append("Telegram > PHONE_NUMBER")
        if not self.USER_ID:
            missing_fields.append("Gifts > USER_ID")
        if not self.GIFT_RANGES:
            missing_fields.append("Ranges (at least one range must be defined)")

        if missing_fields:
            error_message = self.locale.missing_config_error.format(
                '\n'.join(f'- {field}' for field in missing_fields)
            )
            error(error_message)
            sys.exit(1)


config = Config()
