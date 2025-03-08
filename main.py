import asyncio
import traceback
from typing import Set, Dict, Any

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError
from pytz import timezone as _timezone

from data.config import config
from src.banner import title, info, cmd, get_locale
from src.callbacks import new_callback
from utils.common import send_notification, format_number
from utils.detector import detector
from utils.helper import buyer
from utils.logger import info as log_info, error

sent_gift_ids: Set[int] = set()
timezone = _timezone(config.TIMEZONE)
app_info: Dict[str, Any] = info()
language, locale = get_locale(config.LANGUAGE)


async def send_greeting(client: Client, chat_id: int) -> bool:
    try:
        await client.send_message(
            chat_id,
            "👋 Just a quick check-in! Feel free to ignore this message.\n\n"
            "⭐Sent via <a href='https://github.com/bohd4nx/Gifts-Buyer'>Gifts Buyer</a>\n"
            "🧑‍💻Developed by @bohd4nx (@GiftsTracker)",
            disable_web_page_preview=True
        )
        await client.get_users(chat_id)
        return True
    except RPCError:
        return False


async def send_start_message(client: Client) -> None:
    ranges_info = "\n".join([
        f"💰 {min_price}-{max_price} | 🎁 {num_gifts}x | ⚡️ Supply: {format_number(supply)}"
        for min_price, max_price, supply, num_gifts in config.GIFT_RANGES
    ])

    message = f"{locale.start_message.format(ranges_info=ranges_info)}\n\n"
    await send_notification(client, message)


async def process_gifts(client: Client) -> None:
    for gift_id in config.GIFT_IDS:
        if gift_id in sent_gift_ids:
            continue

        for chat_id in config.USER_ID:
            try:
                if await send_greeting(client, chat_id):
                    await buyer(client, chat_id, int(gift_id), locale)
                    await asyncio.sleep(5)
            except RPCError as ex:
                error(locale.purchase_error.format(gift_id, chat_id))
                error(str(ex))

        sent_gift_ids.add(gift_id)


async def main() -> None:
    cmd(app_info)
    title(app_info, language)

    async with Client(
            name=config.SESSION,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER
    ) as client:
        await send_start_message(client)
        await process_gifts(client)
        await detector(client, new_callback, locale)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info(f"{locale.terminated}")
    except Exception:
        error(locale.unexpected_error)
        traceback.print_exc()
