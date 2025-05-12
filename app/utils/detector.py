import asyncio
import json
import time
from typing import Callable, Dict, List, Tuple

from pyrogram import Client, types

from app.core.callbacks import process_skipped_gifts
from app.utils.logger import log_same_line, info
from data.config import config, t


async def _load_old_gifts() -> Dict[int, dict]:
    try:
        with config.DATA_FILEPATH.open("r", encoding='utf-8') as file:
            return {gift["id"]: gift for gift in json.load(file)}
    except FileNotFoundError:
        return {}


async def _save_gifts(gifts: List[dict]) -> None:
    with config.DATA_FILEPATH.open("w", encoding='utf-8') as file:
        json.dump(gifts, file, indent=4, default=types.Object.default, ensure_ascii=False)


async def _get_formatted_gifts(app: Client) -> Tuple[Dict[int, dict], List[int]]:
    all_gifts = [
        json.loads(json.dumps(gift, default=types.Object.default, ensure_ascii=False))
        for gift in await app.get_available_gifts()
    ]

    all_gifts_raw = {gift["id"]: gift for gift in all_gifts}
    return all_gifts_raw, list(all_gifts_raw.keys())


async def detector(app: Client, new_callback: Callable) -> None:
    dot = 0

    while True:
        dot = (dot + 1) % 4
        log_same_line(f'{t("console.gift_checking")}{"." * dot}')
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
            info(f'{t("console.new_gifts")} {len(new_gifts_raw)}')

            all_gifts_amount = len(all_gifts_ids)
            for gift_id, gift_raw in new_gifts_raw.items():
                gift_raw["number"] = all_gifts_amount - all_gifts_ids.index(gift_id)

            for gift_id, gift_raw in sorted(new_gifts_raw.items(), key=lambda it: it[1]["number"]):
                await new_callback(app, gift_raw)

            await process_skipped_gifts(app)

        await _save_gifts(list(all_gifts_raw.values()))
        await asyncio.sleep(config.INTERVAL)
