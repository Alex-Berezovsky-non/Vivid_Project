from django import forms
from django.core.mail import send_mail
from django.conf import settings
import logging
from core.models import Service
from utils.notifications import send_telegram_alert

logger = logging.getLogger(__name__)

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )

    def send_email(self):
        """Отправка email и уведомления в Telegram"""
        # Подготовка данных
        name = self.cleaned_data['name']
        user_email = self.cleaned_data['email']
        message_text = self.cleaned_data['message']
        
        # Формируем полное тело письма
        full_message = (
            f"Сообщение от: {name}\n"
            f"Email для ответа: {user_email}\n\n"
            f"Текст сообщения:\n{message_text}"
        )
        
        # 1. Отправка email через Яндекс SMTP
        try:
            send_mail(
                subject=f"Новое сообщение от {name}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Обязательно ваш Яндекс-адрес
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Ошибка отправки email: {e}")
            raise

        # 2. Отправка в Telegram
        telegram_msg = (
            f"📩 *Новое сообщение с сайта!*\n\n"
            f"*Имя:* {name}\n"
            f"*Email:* `{user_email}`\n\n"
            f"*Сообщение:*\n{message_text[:500]}"  # Ограничение до 500 символов
        )
        
        try:
            send_telegram_alert(telegram_msg)
        except Exception as e:
            logger.error(f"Ошибка отправки Telegram-уведомления: {e}")
            # Не прерываем выполнение, если Telegram недоступен

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }