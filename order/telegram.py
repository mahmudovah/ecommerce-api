import requests
from django.conf import settings


def send_telegram_notification(order):
    """
    Yangi zakaz tushganda Telegram guruhga xabar yuboradi.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    # Zakaz ma'lumotlarini yig'ish
    items_text = ""
    if hasattr(order, 'items'):
        for item in order.items.all():
            items_text += f"  • {item.product.name} x {item.quantity} — {item.price} so'm\n"
    else:
        items_text = "  (mahsulotlar ro'yxati mavjud emas)\n"

    message = (
        f"🛒 <b>Yangi zakaz tushdi!</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📦 <b>Zakaz #</b>{order.id}\n"
        f"👤 <b>Mijoz:</b> {order.user}\n"
        f"📞 <b>Telefon:</b> {order.phone}\n"
        f"📍 <b>Manzil:</b> {order.shipping_address}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🛍 <b>Mahsulotlar:</b>\n{items_text}"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Jami:</b> {order.total_amount} so'm\n"
        f"📊 <b>Status:</b> {order.status}\n"
        f"🕐 <b>Vaqt:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"[Telegram] Xabar yuborishda xatolik: {e}")
        return False