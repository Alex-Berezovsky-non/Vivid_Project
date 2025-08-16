# utils/notifications.py
import os
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from telegram import Bot
from telegram.error import TelegramError
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

async def _async_send_telegram_alert(message: str) -> bool:
    """Асинхронная отправка сообщения в Telegram"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_API_KEY)
        await bot.send_message(
            chat_id=settings.TELEGRAM_USER_ID,
            text=message,
            parse_mode="Markdown"
        )
        return True
    except TelegramError as e:
        logger.error(f"Telegram API error: {e}")
        return False
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        return False

def send_telegram_alert(message: str) -> bool:
    """
    Синхронная обертка для отправки уведомлений
    Использует настройки из settings.py:
    - TELEGRAM_BOT_API_KEY
    - TELEGRAM_USER_ID
    """
    if not hasattr(settings, 'TELEGRAM_BOT_API_KEY'):
        raise ImproperlyConfigured("TELEGRAM_BOT_API_KEY не настроен")
    if not hasattr(settings, 'TELEGRAM_USER_ID'):
        raise ImproperlyConfigured("TELEGRAM_USER_ID не настроен")

    return async_to_sync(_async_send_telegram_alert)(message)