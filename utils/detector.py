import asyncio
import json
import time
from typing import Any, Callable

from pyrogram import Client, types
from pytz import timezone as _timezone

from data.config import config
from utils.logger import log_same_line, info

timezone = _timezone(config.TIMEZONE)


async def _load_old_gifts() -> dict:
    try:
        with config.DATA_FILEPATH.open("r", encoding='utf-8') as file:
            old_gifts_raw = json.load(file)
            return {gift["id"]: gift for gift in old_gifts_raw}
    except FileNotFoundError:
        return {}


async def _save_gifts(gifts: list) -> None:
    with config.DATA_FILEPATH.open("w", encoding='utf-8') as file:
        json.dump(gifts, file, indent=4, default=types.Object.default, ensure_ascii=False)


async def _get_formatted_gifts(app: Client) -> tuple[dict, list]:
    all_gifts = [
        json.loads(json.dumps(gift, indent=4, default=types.Object.default, ensure_ascii=False))
        for gift in await app.get_available_gifts()
    ]

    all_gifts_raw = {gift["id"]: gift for gift in all_gifts}
    all_gifts_ids = list(all_gifts_raw.keys())

    return all_gifts_raw, all_gifts_ids


async def detector(app: Client, new_callback: Callable, locale: Any) -> None:
    dot = 0

    while True:
        dot = (dot + 1) % 4
        log_same_line(f'{locale.gift_checking}{"." * dot}')

        time.sleep(0.2)

        if not app.is_connected:
            await app.start()

        old_gifts = await _load_old_gifts()
        all_gifts_raw, all_gifts_ids = await _get_formatted_gifts(app)

        new_gifts_raw = {
            key: value for key, value in all_gifts_raw.items()
            if key not in old_gifts
        }

        if new_gifts_raw:
            print("\n\n")
            info(f'{locale.new_gifts} {len(new_gifts_raw)}')
            print("\n\n")

            all_gifts_amount = len(all_gifts_ids)
            for gift_id, gift_raw in new_gifts_raw.items():
                gift_raw["number"] = all_gifts_amount - all_gifts_ids.index(gift_id)

            for gift_id, gift_raw in sorted(new_gifts_raw.items(), key=lambda it: it[1]["number"]):
                await new_callback(app, gift_raw, locale)

        await _save_gifts(list(all_gifts_raw.values()))

        await asyncio.sleep(config.INTERVAL)
