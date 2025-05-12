import asyncio
import traceback

from pyrogram import Client
from pytz import timezone as _timezone

from app.core.banner import title, info, cmd
from app.core.callbacks import new_callback
from app.notifications import send_start_message
from app.utils.detector import detector
from app.utils.logger import info as log_info, error
from data.config import config, t, get_language_display

timezone = _timezone(config.TIMEZONE)
app_info = info()


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
        log_info(t("console.terminated"))
    except Exception:
        error(t("console.unexpected_error"))
        traceback.print_exc()
