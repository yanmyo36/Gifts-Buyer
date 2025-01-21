import asyncio
from typing import Tuple

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError

import config
from src.notifications import notifications


async def _handle_error(app: Client, ex: RPCError, star_gift_id: int, chat_id: int, num: int) -> None:
    """
    Handle various Telegram API errors that may occur during gift sending.
    
    Args:
        app (Client): Telegram client instance
        ex (RPCError): Exception that occurred
        star_gift_id (int): ID of the gift that failed
        chat_id (int): ID of chat where error occurred
        num (int): Total number of gifts being sent
    """
    locale = config.locale
    error_message = f"<pre>{str(ex)}</pre>"

    error_handlers = {
        'BALANCE_TOO_LOW': {
            'check': lambda e: 'BALANCE_TOO_LOW' in str(e) or '400 BALANCE_TOO_LOW' in str(e),
            'message': lambda: f"\n\033[91m[ ERROR ]\033[0m {locale.low_balance}\n",
            'notification': lambda: {'balance_error': True}
        },
        'STARGIFT_USAGE_LIMITED': {
            'check': lambda e: 'STARGIFT_USAGE_LIMITED' in str(e),
            'message': lambda: f"\033[91m[ ERROR ]\033[0m {locale.out_of_stock.format(star_gift_id)}\n",
            'notification': lambda: {'usage_limited': True}
        },
        'PEER_ID_INVALID': {
            'check': lambda e: 'PEER_ID_INVALID' in str(e),
            'message': lambda: f"\n\033[91m[ ERROR ]\033[0m {locale.peer_id}\n",
            'notification': lambda: {'peer_id_error': True}
        }
    }

    for handler in error_handlers.values():
        if handler['check'](ex):
            print(handler['message']())
            await notifications(app, star_gift_id, total_gifts=num, **handler['notification']())
            return

    print(f"\n\033[91m[ ERROR ]\033[0m {locale.gift_send_error.format(star_gift_id, chat_id)}\n{str(ex)}\n")
    await notifications(app, star_gift_id, error_message=error_message, total_gifts=num)


async def _get_recipient_info(app: Client, chat_id: int) -> Tuple[str, str]:
    """
    Get recipient information from chat ID.
    
    Args:
        app: Telegram client instance
        chat_id: User's chat ID
        
    Returns:
        Tuple[str, str]: (formatted recipient info, username)
    """
    user = await app.get_chat(chat_id)
    username = user.username or ""

    recipient_info = (
        f"@{username.strip()}" if username
        else f"{chat_id}" if str(chat_id)[0].isdigit()
        else f"@{str(chat_id).strip()}"
    )

    return recipient_info, username


async def _send_single_gift(app: Client, chat_id: int, star_gift_id: int, recipient_info: str, username: str,
                            current_gift: int, total_gifts: int, hide_my_name: bool
                            ) -> None:
    """
    Send a single gift and handle notifications.
    
    Args:
        app: Telegram client instance
        chat_id: Recipient's chat ID
        star_gift_id: Gift ID to send
        recipient_info: Formatted recipient info
        username: Recipient's username
        current_gift: Current gift number
        total_gifts: Total gifts to send
        hide_my_name: Whether to hide sender name
    """
    await app.send_star_gift(chat_id=chat_id, star_gift_id=star_gift_id, hide_my_name=hide_my_name)

    print(
        f"\033[93m[ ★ ]\033[0m {config.locale.gift_sent.format(current_gift, total_gifts, star_gift_id, recipient_info)}\n")

    if config.GIFT_DELAY > 0:
        await notifications(app, star_gift_id, user_id=chat_id, username=username, current_gift=current_gift,
                            total_gifts=total_gifts)


async def buyer(app: Client, chat_id: int, star_gift_id: int, hide_my_name: bool = config.HIDE_SENDER_NAME) -> None:
    """
    Purchase and send multiple star gifts to specified user.
    
    Args:
        app: Telegram client instance
        chat_id: User ID to send gift to
        star_gift_id: ID of gift to send
        hide_my_name: Whether to hide sender name
    """
    # Initialize total_gifts with default value
    total_gifts = 1

    try:
        recipient_info, username = await _get_recipient_info(app, chat_id)
        all_gifts = await app.get_star_gifts()
        gift_info = next((gift for gift in all_gifts if gift.id == star_gift_id), None)

        if not gift_info:
            return

        total_amount = getattr(gift_info, 'total_amount', 0) or 0
        gift_price = getattr(gift_info, 'price', 0) or 0

        for min_price, max_price, supply_limit, num_gifts in config.GIFT_RANGES:
            if min_price <= gift_price < max_price:
                if total_amount > supply_limit:
                    print(f"\n\033[91m[ ERROR ]\033[0m Supply limit exceeded: {total_amount} > {supply_limit}")
                    return
                total_gifts = num_gifts
                break

        for i in range(total_gifts):
            current_gift = i + 1

            await _send_single_gift(app=app, chat_id=chat_id, star_gift_id=star_gift_id, recipient_info=recipient_info,
                                    username=username, current_gift=current_gift, total_gifts=total_gifts,
                                    hide_my_name=hide_my_name)
            if i < total_gifts - 1 and config.GIFT_DELAY > 0:
                await asyncio.sleep(config.GIFT_DELAY)

    except RPCError as ex:
        await _handle_error(app, ex, star_gift_id, chat_id, total_gifts)
