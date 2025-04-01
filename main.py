import asyncio
import traceback
from typing import Set

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError
from pytz import timezone as _timezone

from data.config import config, _, get_language_display
from src.banner import title, info, cmd
from src.callbacks import new_callback
from utils.common import send_notification
from utils.detector import detector
from utils.helper import get_user_balance
from utils.logger import info as log_info, error

sent_gift_ids: Set[int] = set()
timezone = _timezone(config.TIMEZONE)
app_info = info()


async def send_greeting(client: Client, chat_id: int) -> bool:
    try:
        await client.send_message(
            chat_id,
            "👋 Just a quick check-in! Feel free to ignore this message.\n\n"
            "⭐Sent via <a href='https://github.com/bohd4nx/Gifts-Buyer'>Gifts Buyer</a>\n"
            "🧑‍💻Developed by @bohd4nx | @AccessCheckerBot & @WhoseGiftBot",
            disable_web_page_preview=True
        )
        await client.get_users(chat_id)
        return True
    except RPCError:
        return False


async def send_start_message(client: Client) -> None:
    balance = await get_user_balance(client)
    message = _("telegram.start_message",
                language=config.LANGUAGE_DISPLAY,
                locale=config.LANGUAGE,
                balance=balance,
                min_price=config.MIN_GIFT_PRICE,
                max_price=config.MAX_GIFT_PRICE,
                quantity=config.GIFT_QUANTITY)
    await send_notification(client, message)


async def main() -> None:
    cmd(app_info)
    title(app_info, get_language_display(config.LANGUAGE))

    async with Client(
            name=config.SESSION,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER
    ) as client:
        await send_start_message(client)
        await detector(client, new_callback)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info(_("console.terminated"))
    except Exception:
        error(_("console.unexpected_error"))
        traceback.print_exc()
