from typing import Optional

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError

from data.config import config
from utils.logger import error


def format_user_reference(user_id: int, username: Optional[str] = None) -> str:
    if username:
        return f"@{username} | <code>{user_id}</code>"
    if isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit()):
        return f'<a href="tg://user?id={user_id}">{user_id}</a>'
    return f"@{user_id}" if isinstance(user_id, str) else str(user_id)


async def send_notification(app: Client, message: str, disable_web_page_preview: bool = True) -> None:
    try:
        if config.CHANNEL_ID:
            await app.send_message(
                config.CHANNEL_ID,
                message,
                disable_web_page_preview=disable_web_page_preview
            )
    except RPCError as ex:
        error(f'Failed to send notification: {str(ex)}')


def format_number(num: int) -> str:
    if num >= 1000000:
        return f"{num / 1000000:.1f}m".rstrip('0').rstrip('.')
    elif num >= 1000:
        return f"{num / 1000:.1f}k".rstrip('0').rstrip('.')
    return str(num)
