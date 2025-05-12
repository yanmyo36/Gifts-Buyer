from pyrogram import Client
from pyrogram.errors import RPCError

from app.errors import handle_gift_error
from app.notifications import send_notification
from data.config import config, t
from utils.helper import get_recipient_info, get_user_balance
from utils.logger import success


async def buy_gift(app: Client, chat_id: int, gift_id: int) -> None:
    total_gifts = config.GIFT_QUANTITY

    try:
        recipient_info, username = await get_recipient_info(app, chat_id)

        for i in range(total_gifts):
            current_gift = i + 1

            await app.send_gift(chat_id=chat_id, gift_id=gift_id, hide_my_name=True)

            success(t("console.gift_sent", current=current_gift, total=total_gifts,
                      gift_id=gift_id, recipient=recipient_info))

            await send_notification(app, gift_id, user_id=chat_id, username=username,
                                    current_gift=current_gift)

    except RPCError as ex:
        gift_price = 0
        current_balance = 0

        try:
            gifts = await app.get_available_gifts()
            for gift in gifts:
                if gift.id == gift_id:
                    gift_price = gift.price
                    break

            current_balance = await get_user_balance(app)
        except Exception:
            pass

        await handle_gift_error(app, ex, gift_id, chat_id, gift_price, current_balance)
