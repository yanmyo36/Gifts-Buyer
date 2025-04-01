import asyncio
from typing import Tuple

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError

from data.config import config, _
from src.notifications import notifications
from utils.logger import error, success


async def get_user_balance(client: Client) -> int:
    try:
        return await client.get_stars_balance()
    except Exception:
        return 0


async def _handle_error(app: Client, ex: RPCError, gift_id: int, chat_id: int, num: int) -> None:
    error_message = f"<pre>{str(ex)}</pre>"

    gift_price = 0
    current_balance = 0

    try:
        gifts = await app.get_available_gifts()
        for gift in gifts:
            if gift.id == gift_id:
                gift_price = gift.price
                break

        current_balance = await get_user_balance(app)
    except Exception:
        pass

    error_handlers = {
        'BALANCE_TOO_LOW': {
            'check': lambda e: 'BALANCE_TOO_LOW' in str(e) or '400 BALANCE_TOO_LOW' in str(e),
            'message': lambda: _("console.low_balance"),
            'notification': lambda: {'balance_error': True, 'gift_price': gift_price,
                                     'current_balance': current_balance}
        },
        'STARGIFT_USAGE_LIMITED': {
            'check': lambda e: 'STARGIFT_USAGE_LIMITED' in str(e),
            'message': lambda: _("console.out_of_stock", gift_id=gift_id),
            'notification': lambda: {}
        },
        'PEER_ID_INVALID': {
            'check': lambda e: 'PEER_ID_INVALID' in str(e),
            'message': lambda: _("console.peer_id"),
            'notification': lambda: {'peer_id_error': True}
        }
    }

    for handler in error_handlers.values():
        if handler['check'](ex):
            if handler['message']():
                error(handler['message']())
            if handler['notification']():
                await notifications(app, gift_id, total_gifts=num, **handler['notification']())
            return

    error(_("console.gift_send_error", gift_id=gift_id, chat_id=chat_id))
    error(str(ex))
    await notifications(app, gift_id, error_message=error_message, total_gifts=num)


async def _get_recipient_info(app: Client, chat_id: int) -> Tuple[str, str]:
    user = await app.get_chat(chat_id)
    username = user.username or ""

    recipient_info = (
        f"@{username.strip()}" if username
        else f"{chat_id}" if isinstance(chat_id, int) or str(chat_id).isdigit()
        else f"@{chat_id}"
    )

    return recipient_info, username


async def buyer(app: Client, chat_id: int, gift_id: int, hide_my_name: bool = None) -> None:
    if hide_my_name is None:
        hide_my_name = config.HIDE_SENDER_NAME

    total_gifts = config.GIFT_QUANTITY

    try:
        recipient_info, username = await _get_recipient_info(app, chat_id)

        for i in range(total_gifts):
            current_gift = i + 1

            await app.send_gift(chat_id=chat_id, gift_id=gift_id, hide_my_name=hide_my_name)

            success(_("console.gift_sent", current=current_gift, total=total_gifts,
                      gift_id=gift_id, recipient=recipient_info))

            if config.GIFT_DELAY > 0 and i < total_gifts - 1:
                await notifications(app, gift_id, user_id=chat_id, username=username,
                                    current_gift=current_gift, total_gifts=total_gifts)
                await asyncio.sleep(config.GIFT_DELAY)

    except RPCError as ex:
        await _handle_error(app, ex, gift_id, chat_id, total_gifts)
