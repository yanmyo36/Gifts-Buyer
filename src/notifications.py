from pyrogram import Client

from data.config import config, _
from utils.common import format_user_reference, send_notification


async def notifications(app: Client, gift_id: int, **kwargs) -> None:
    num = config.GIFT_QUANTITY

    message_formatters = {
        'peer_id_error': lambda: _("telegram.peer_id_error"),
        'error_message': lambda: _("telegram.error_message", error=kwargs.get('error_message')),
        'balance_error': lambda: _("telegram.balance_error",
                                   gift_id=gift_id,
                                   gift_price=kwargs.get('gift_price', 0),
                                   current_balance=kwargs.get('current_balance', 0)),
        'sold_out': lambda: _("telegram.sold_out_error", gift_id=gift_id),
        'sold_out_summary': lambda: _("telegram.sold_out_summary", count=kwargs.get('count', 0)),
        'non_limited_error': lambda: _("telegram.non_limited_error", gift_id=gift_id),
        'non_limited_summary': lambda: _("telegram.non_limited_summary", count=kwargs.get('count', 0)),
        'non_upgradable_error': lambda: _("telegram.non_upgradable_error", gift_id=gift_id),
        'non_upgradable_summary': lambda: _("telegram.non_upgradable_summary", count=kwargs.get('count', 0)),
        'gift_price': lambda: _("telegram.gift_price", gift_id=gift_id, price=kwargs.get('gift_price'),
                                supply=kwargs.get('gift_supply') or "N/A"),
        'success_message': lambda: _("telegram.success_message", current=kwargs.get('current_gift'),
                                     total=num, gift_id=gift_id, recipient='') +
                                   format_user_reference(kwargs.get('user_id'), kwargs.get('username'))
    }

    conditions = {
        'peer_id_error': kwargs.get('peer_id_error'),
        'error_message': kwargs.get('error_message'),
        'balance_error': kwargs.get('balance_error'),
        'sold_out': kwargs.get('sold_out'),
        'sold_out_summary': kwargs.get('sold_out_summary'),
        'non_limited_error': kwargs.get('non_limited_error'),
        'non_limited_summary': kwargs.get('non_limited_summary'),
        'non_upgradable_error': kwargs.get('non_upgradable_error'),
        'non_upgradable_summary': kwargs.get('non_upgradable_summary'),
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
