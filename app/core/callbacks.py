import asyncio
from typing import Dict, Tuple, Any

from pyrogram import Client

from app.notifications import send_notification
from app.purchase import buy_gift
from app.utils.logger import warn, info
from data.config import config, t

_counters = {
    'sold_out': 0,
    'non_limited': 0,
    'non_upgradable': 0
}


class GiftFilter:
    @staticmethod
    async def is_eligible(gift_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        gift_price = gift_data.get("price", 0)
        is_limited = gift_data.get("is_limited", False)
        is_sold_out = gift_data.get("is_sold_out", False)
        is_upgradable = "upgrade_price" in gift_data
        total_amount = gift_data.get("total_amount", "N/A") if is_limited else "N/A"

        validation_rules = [
            {
                'condition': is_sold_out,
                'counter': 'sold_out',
                'return_data': {}
            },
            {
                'condition': not is_limited and not config.PURCHASE_NON_LIMITED_GIFTS,
                'counter': 'non_limited',
                'return_data': {}
            },
            {
                'condition': config.PURCHASE_ONLY_UPGRADABLE_GIFTS and not is_upgradable,
                'counter': 'non_upgradable',
                'return_data': {}
            },
            {
                'condition': not (config.MIN_GIFT_PRICE <= gift_price <= config.MAX_GIFT_PRICE),
                'counter': None,
                'return_data': {
                    "gift_price_error": True,
                    "gift_price": gift_price,
                    "total_amount": total_amount
                }
            }
        ]

        for rule in validation_rules:
            if rule['condition']:
                if rule['counter']:
                    _counters[rule['counter']] += 1
                return False, rule['return_data']

        return True, {}


async def new_callback(app: Client, gift_data: Dict[str, Any]) -> None:
    gift_id = gift_data.get("id")
    is_eligible, notification_kwargs = await GiftFilter.is_eligible(gift_data)

    if not is_eligible:
        if notification_kwargs:
            await send_notification(app, gift_id, **notification_kwargs)
        return

    for user_id in config.USER_ID:
        try:
            await buy_gift(app, user_id, gift_id)
        except Exception as ex:
            warn(t("console.purchase_error", gift_id=gift_id, chat_id=user_id))
            await send_notification(app, gift_id, error_message=str(ex))
        await asyncio.sleep(0.5)


async def process_skipped_gifts(app: Client) -> None:
    notifications = [
        ('sold_out', 'sold_out_summary', 'console.sold_out_gifts_summary'),
        ('non_limited', 'non_limited_summary', 'console.non_limited_gifts_summary'),
        ('non_upgradable', 'non_upgradable_summary', 'console.non_upgradable_gifts_summary')
    ]

    for counter_key, notif_key, console_key in notifications:
        count = _counters[counter_key]
        if count > 0:
            info(t(console_key, count=count))
            await send_notification(app, 0, **{notif_key: True, 'count': count})
            _counters[counter_key] = 0
