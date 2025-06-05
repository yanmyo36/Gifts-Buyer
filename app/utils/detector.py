import asyncio
import json
import time
from typing import Callable, Dict, List, Tuple

from pyrogram import Client, types

from app.core.callbacks import process_skipped_gifts
from app.utils.logger import log_same_line, info
from data.config import config, t


async def load_old_gifts() -> Dict[int, dict]:
    try:
        with config.DATA_FILEPATH.open("r", encoding='utf-8') as file:
            return {gift["id"]: gift for gift in json.load(file)}
    except FileNotFoundError:
        return {}


async def save_gifts(gifts: List[dict]) -> None:
    with config.DATA_FILEPATH.open("w", encoding='utf-8') as file:
        json.dump(gifts, file, indent=4, default=types.Object.default, ensure_ascii=False)


async def get_current_gifts(app: Client) -> Tuple[Dict[int, dict], List[int]]:
    gifts = [
        json.loads(json.dumps(gift, default=types.Object.default, ensure_ascii=False))
        for gift in await app.get_available_gifts()
    ]
    gifts_dict = {gift["id"]: gift for gift in gifts}
    return gifts_dict, list(gifts_dict.keys())


async def detector(app: Client, callback: Callable) -> None:
    dot_count = 0

    while True:
        dot_count = (dot_count + 1) % 4
        log_same_line(f'{t("console.gift_checking")}{"." * dot_count}')
        time.sleep(0.2)

        if not app.is_connected:
            await app.start()

        old_gifts = await load_old_gifts()
        current_gifts, gift_ids = await get_current_gifts(app)

        new_gifts = {
            gift_id: gift_data for gift_id, gift_data in current_gifts.items()
            if gift_id not in old_gifts
        }

        if new_gifts:
            info(f'{t("console.new_gifts")} {len(new_gifts)}')

            total_gifts = len(gift_ids)
            for gift_id, gift_data in new_gifts.items():
                gift_data["number"] = total_gifts - gift_ids.index(gift_id)

            sorted_gifts = sorted(new_gifts.items(), key=lambda x: x[1]["number"])
            for gift_id, gift_data in sorted_gifts:
                await callback(app, gift_data)

            await process_skipped_gifts(app)

        await save_gifts(list(current_gifts.values()))
        await asyncio.sleep(config.INTERVAL)
