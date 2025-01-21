from pyrogram import Client

import config
from utils.common import format_user_reference, send_notification


async def notifications(app: Client, star_gift_id: int, **kwargs) -> None:
    """
    Send notification messages about gift operations to logging channel.
    
    Args:
        app (Client): Telegram client instance
        star_gift_id (int): ID of gift being processed
        **kwargs: Various optional parameters that determine notification type:
            - gift_price (float): Price of the gift
            - user_id (int): User ID gift was sent to
            - username (str): Username gift was sent to
            - balance_error (bool): Whether error was due to insufficient balance
            - error_message (str): Custom error message
            - non_limited_error (bool): Whether error was due to non-limited gift
            - current_gift (int): Current gift number in sequence
            - usage_limited (bool): Whether gift is no longer available
            - peer_id_error (bool): Whether error was due to invalid peer
            - total_gifts (int): Total gifts in sequence
            - gift_supply (int): Available supply of gift
    """
    locale = config.locale
    all_gifts = await app.get_star_gifts()
    gift_info = next((gift for gift in all_gifts if gift.id == star_gift_id), None)
    num = config.get_num_gifts(gift_info.price)

    message_formatters = {
        'peer_id_error': lambda: locale.peer_id_error,
        'error_message': lambda: locale.error_message.format(kwargs.get('error_message')),
        'balance_error': lambda: locale.balance_error.format(star_gift_id),
        'usage_limited': lambda: locale.usage_limited.format(star_gift_id),
        'non_limited_error': lambda: locale.non_limited_error.format(star_gift_id),
        'gift_price': lambda: locale.gift_price.format(star_gift_id, kwargs.get('gift_price'),
                                                       kwargs.get('gift_supply') or "N/A"),
        'success_message': lambda: locale.success_message.format(kwargs.get('current_gift'), num, star_gift_id, '') +
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
