from typing import Any

from pyrogram import Client

from data.config import config
from utils.common import format_user_reference, send_notification, find_gift_by_id


async def notifications(app: Client, gift_id: int, locale: Any = None, **kwargs) -> None:
    if locale is None:
        from src.banner import get_locale
        _, locale = get_locale(config.LANGUAGE)

    gift_info = await find_gift_by_id(app, gift_id)
    num = config.get_num_gifts(getattr(gift_info, 'price', 0) or 0) if gift_info else 1

    message_formatters = {
        'peer_id_error': lambda: locale.peer_id_error,
        'error_message': lambda: locale.error_message.format(kwargs.get('error_message')),
        'balance_error': lambda: locale.balance_error.format(gift_id),
        'usage_limited': lambda: locale.usage_limited.format(gift_id),
        'non_limited_error': lambda: locale.non_limited_error.format(gift_id),
        'gift_price': lambda: locale.gift_price.format(gift_id, kwargs.get('gift_price'),
                                                       kwargs.get('gift_supply') or "N/A"),
        'success_message': lambda: locale.success_message.format(kwargs.get('current_gift'), num, gift_id, '') +
                                   format_user_reference(kwargs.get('user_id'), kwargs.get('username'))
    }

    conditions = {
        'peer_id_error': kwargs.get('peer_id_error'),
        'error_message': kwargs.get('error_message'),
        'balance_error': kwargs.get('balance_error'),
        'usage_limited': kwargs.get('usage_limited'),
        'non_limited_error': kwargs.get('non_limited_error'),
        'gift_price': kwargs.get('gift_price'),
        'success_message': kwargs.get('current_gift')
    }

    message = None
    for condition_name, condition_value in conditions.items():
        if condition_value:
            message = message_formatters[condition_name]()
            break

    if message:
        await send_notification(app, message.strip())
