from datetime import datetime
from typing import Optional

from pyrogram import Client
from pyrogram.errors.exceptions import RPCError
from pytz.tzinfo import BaseTzInfo

import config


def get_time(timezone: BaseTzInfo) -> str:
    """
    Get current time formatted according to specified timezone.
    
    Args:
        timezone (BaseTzInfo): Timezone to format time in
        
    Returns:
        str: Formatted time string
    """
    return datetime.now().astimezone(timezone).strftime("%d.%m.%y :: %H:%M:%S")


def format_user_reference(user_id: int, username: Optional[str] = None) -> str:
    """
    Format user reference for notifications with proper HTML formatting.
    
    Args:
        user_id: User's Telegram ID
        username: Optional username
        
    Returns:
        str: Formatted user reference string
    """
    if username:
        return f"@{username} | <code>{user_id}</code>"
    if str(user_id).isdigit():
        return f'<a href="tg://user?id={user_id}">{user_id}</a>'
    return f"@{user_id.strip()}"


async def send_notification(
        app: Client,
        message: str,
        disable_web_page_preview: bool = True
) -> None:
    """
    Send notification message to configured channel.
    
    Args:
        app: Telegram client instance
        message: Message to send
        disable_web_page_preview: Whether to disable link previews
    """
    try:
        if config.CHANNEL_ID:
            await app.send_message(
                config.CHANNEL_ID,
                message,
                disable_web_page_preview=disable_web_page_preview
            )
    except RPCError as ex:
        print(f"\n\033[91m[ ERROR ]\033[0m Failed to send notification: {str(ex)}\n")


def format_number(num: int) -> str:
    """Convert number to k/m format"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}m".rstrip('0').rstrip('.')
    elif num >= 1000:
        return f"{num / 1000:.1f}k".rstrip('0').rstrip('.')
    return str(num)
