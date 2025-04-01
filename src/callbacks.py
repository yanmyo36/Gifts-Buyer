import asyncio
from collections import defaultdict

from pyrogram import Client

from data.config import config, _
from src.notifications import notifications
from utils.helper import buyer
from utils.logger import warn

sent_gift_ids = set()
skipped_gifts = defaultdict(list)


def _is_gift_within_limits(gift_price: float) -> bool:
    return config.MIN_GIFT_PRICE <= gift_price <= config.MAX_GIFT_PRICE


def _is_gift_upgradable(gift_raw: dict) -> bool:
    return "upgrade_price" in gift_raw and gift_raw["upgrade_price"] is not None


def _handle_limited_gift(gift_id: int) -> bool:
    if gift_id in sent_gift_ids:
        return False
    sent_gift_ids.add(gift_id)
    return True


def _handle_non_limited_gift(gift_id: int, gift_price: float) -> bool:
    if not config.PURCHASE_NON_LIMITED_GIFTS or gift_price > config.MAX_GIFT_PRICE:
        return False
    if gift_id not in sent_gift_ids:
        sent_gift_ids.add(gift_id)
        return True
    return False


async def process_skipped_gifts(app: Client) -> None:
    if skipped_gifts['sold_out']:
        count = len(skipped_gifts['sold_out'])
        warn(_("console.sold_out_gifts_summary", count=count))
        await notifications(app, 0, sold_out_summary=True, count=count)

    if skipped_gifts['non_limited']:
        count = len(skipped_gifts['non_limited'])
        warn(_("console.non_limited_gifts_summary", count=count))
        await notifications(app, 0, non_limited_summary=True, count=count)

    if skipped_gifts['non_upgradable']:
        count = len(skipped_gifts['non_upgradable'])
        warn(_("console.non_upgradable_gifts_summary", count=count))
        await notifications(app, 0, non_upgradable_summary=True, count=count)

    skipped_gifts.clear()


async def new_callback(app: Client, gift_raw: dict) -> None:
    gift_price = gift_raw.get("price", 0)
    gift_id = gift_raw['id']

    if _should_skip_gift(app, gift_raw, gift_price, gift_id):
        return

    is_limited = gift_raw.get("is_limited", False)
    if is_limited and not _handle_limited_gift(gift_id):
        return

    if not is_limited and not _handle_non_limited_gift(gift_id, gift_price):
        skipped_gifts['non_limited'].append(gift_id)
        return

    await _send_gift_to_recipients(app, gift_id)


def _should_skip_gift(app: Client, gift_raw: dict, gift_price: float, gift_id: int) -> bool:
    if gift_raw.get("is_sold_out", False):
        skipped_gifts['sold_out'].append(gift_id)
        return True

    if config.PURCHASE_ONLY_UPGRADABLE_GIFTS and not _is_gift_upgradable(gift_raw):
        skipped_gifts['non_upgradable'].append(gift_id)
        return True

    if not _is_gift_within_limits(gift_price):
        warn(_("console.gift_expensive", gift_id=gift_id))
        asyncio.create_task(notifications(app, gift_id, gift_price=gift_price))
        return True

    return False


async def _send_gift_to_recipients(app: Client, gift_id: int) -> None:
    for i, chat_id in enumerate(config.USER_ID):
        await buyer(app, chat_id, gift_id)
        if i < len(config.USER_ID) - 1:
            await asyncio.sleep(config.GIFT_DELAY)
