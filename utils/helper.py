import asyncio
from typing import Tuple, Any

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError

from data.config import config
from src.notifications import notifications
from utils.common import find_gift_by_id
from utils.logger import error, success


async def _handle_error(app: Client, ex: RPCError, gift_id: int, chat_id: int, num: int, locale: Any) -> None:
    error_message = f"<pre>{str(ex)}</pre>"

    error_handlers = {
        'BALANCE_TOO_LOW': {
            'check': lambda e: 'BALANCE_TOO_LOW' in str(e) or '400 BALANCE_TOO_LOW' in str(e),
            'message': lambda: locale.low_balance,
            'notification': lambda: {'balance_error': True}
        },
        'STARGIFT_USAGE_LIMITED': {
            'check': lambda e: 'STARGIFT_USAGE_LIMITED' in str(e),
            'message': lambda: locale.out_of_stock.format(gift_id),
            'notification': lambda: {'usage_limited': True}
        },
        'PEER_ID_INVALID': {
            'check': lambda e: 'PEER_ID_INVALID' in str(e),
            'message': lambda: locale.peer_id,
            'notification': lambda: {'peer_id_error': True}
        }
    }

    for handler in error_handlers.values():
        if handler['check'](ex):
            error(handler['message']())
            await notifications(app, gift_id, total_gifts=num, locale=locale, **handler['notification']())
            return

    error(locale.gift_send_error.format(gift_id, chat_id))
    error(str(ex))
    await notifications(app, gift_id, error_message=error_message, total_gifts=num, locale=locale)


async def _get_recipient_info(app: Client, chat_id: int) -> Tuple[str, str]:
    user = await app.get_chat(chat_id)
    username = user.username or ""

    recipient_info = (
        f"@{username.strip()}" if username
        else f"{chat_id}" if isinstance(chat_id, int) or str(chat_id).isdigit()
        else f"@{chat_id}"
    )

    return recipient_info, username


async def buyer(app: Client, chat_id: int, gift_id: int, locale: Any, hide_my_name: bool = None) -> None:
    if hide_my_name is None:
        hide_my_name = config.HIDE_SENDER_NAME

    total_gifts = 1

    try:
        recipient_info, username = await _get_recipient_info(app, chat_id)
        gift_info = await find_gift_by_id(app, gift_id)

        if not gift_info:
            return

        gift_price = getattr(gift_info, 'price', 0) or 0
        total_amount = getattr(gift_info, 'total_amount', 0) or 0

        for min_price, max_price, supply_limit, num_gifts in config.GIFT_RANGES:
            if min_price <= gift_price < max_price:
                if total_amount and total_amount > supply_limit:
                    error(f'Supply limit exceeded: {total_amount} > {supply_limit}')
                    return
                total_gifts = num_gifts
                break

        for i in range(total_gifts):
            current_gift = i + 1

            await app.send_gift(chat_id=chat_id, gift_id=gift_id, hide_my_name=hide_my_name)

            success(locale.gift_sent.format(current_gift, total_gifts, gift_id, recipient_info))

            if config.GIFT_DELAY > 0 and i < total_gifts - 1:
                await notifications(app, gift_id, user_id=chat_id, username=username,
                                    current_gift=current_gift, total_gifts=total_gifts, locale=locale)
                await asyncio.sleep(config.GIFT_DELAY)

    except RPCError as ex:
        await _handle_error(app, ex, gift_id, chat_id, total_gifts, locale)
