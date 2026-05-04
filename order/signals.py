from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_notification


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    """Yangi zakaz yaratilganda Telegram guruhga xabar yuboradi."""
    # if created:
    #     send_telegram_notification(instance)
    pass