from typing import Dict, Any

from pyrogram import Client
from pyrogram.errors import RPCError

from app.notifications import send_notification
from app.utils.logger import error
from data.config import t


async def handle_gift_error(app: Client, ex: RPCError, gift_id: int, chat_id: int,
                            gift_price: int = 0, current_balance: int = 0) -> None:
    error_message = f"<pre>{str(ex)}</pre>"

    error_types: Dict[str, Dict[str, Any]] = {
        'BALANCE_TOO_LOW': {
            'check': lambda e: 'BALANCE_TOO_LOW' in str(e),
            'log': t("console.low_balance"),
            'notify': {'balance_error': True, 'gift_price': gift_price, 'current_balance': current_balance}
        },
        'STARGIFT_USAGE_LIMITED': {
            'check': lambda e: 'STARGIFT_USAGE_LIMITED' in str(e),
            'log': t("console.out_of_stock", gift_id=gift_id),
            'notify': {'sold_out': True}
        },
        'PEER_ID_INVALID': {
            'check': lambda e: 'PEER_ID_INVALID' in str(e),
            'log': t("console.peer_id"),
            'notify': {'peer_id_error': True}
        }
    }

    for error_type, handler in error_types.items():
        if handler['check'](ex):
            if handler['log']:
                error(handler['log'])
            if handler['notify']:
                await send_notification(app, gift_id, **handler['notify'])
            return

    error(t("console.gift_send_error", gift_id=gift_id, chat_id=chat_id))
    error(str(ex))
    await send_notification(app, gift_id, error_message=error_message)
