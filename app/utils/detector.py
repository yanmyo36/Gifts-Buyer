import asyncio
import json
import time
from typing import Callable, Dict, List, Tuple

from pyrogram import Client, types

from app.notifications import send_summary_message
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
            skip_counts = {
                'sold_out_count': 0,
                'non_limited_count': 0,
                'non_upgradable_count': 0
            }

            for gift_id, gift_data in new_gifts.items():
                gift_data["number"] = total_gifts - gift_ids.index(gift_id)

                if gift_data.get("is_sold_out"):
                    skip_counts['sold_out_count'] += 1
                elif not gift_data.get("is_limited") and not config.PURCHASE_NON_LIMITED_GIFTS:
                    skip_counts['non_limited_count'] += 1
                elif config.PURCHASE_ONLY_UPGRADABLE_GIFTS and "upgrade_price" not in gift_data:
                    skip_counts['non_upgradable_count'] += 1

            sorted_gifts = sorted(new_gifts.items(), key=lambda x: x[1]["number"])
            for gift_id, gift_data in sorted_gifts:
                await callback(app, gift_data)

            await send_summary_message(app, **skip_counts)

        await save_gifts(list(current_gifts.values()))
        await asyncio.sleep(config.INTERVAL)
