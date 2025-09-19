from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    """Настройки сайта"""
    title = models.CharField(_("Заголовок сайта"), max_length=200)
    phone = models.CharField(_("Телефон"), max_length=20)
    email = models.EmailField(_("Email"))
    instagram = models.URLField(_("Instagram"), blank=True)
    telegram = models.URLField(_("Telegram"), blank=True)
    whatsapp = models.URLField(_("WhatsApp"), blank=True)
    vk = models.URLField(_("VKontakte"), blank=True)
    about_text = models.TextField(_("Текст о фотографе"))
    photographer_photo = models.ImageField(
        _("Фото фотографа"),
        upload_to='about/',
        blank=True,
        null=True,
        help_text=_("Фото для страницы 'Обо мне'")
    )
    footer_about = models.TextField(
        _("Текст в футере"), 
        blank=True,
        help_text=_("Краткое описание для футера (необязательно)")
    )
    address = models.CharField(
        _("Адрес"), 
        max_length=200, 
        blank=True,
        help_text=_("Адрес студии или место съемок")
    )
    copyright_text = models.CharField(
        _("Текст копирайта"), 
        max_length=200, 
        default="Фотограф. Все права защищены."
    )

    class Meta:
        verbose_name = _("Настройки")
        verbose_name_plural = _("Настройки")

    def __str__(self):
        return self.title

    @classmethod
    def load(cls) -> 'SiteSettings':
        obj, created = cls.objects.get_or_create(
            defaults={
                'title': _("Фотограф"),
                'phone': '',
                'email': '',
                'about_text': '',
                'copyright_text': 'Фотограф. Все права защищены.'
            }
        )
        return obj

class Service(models.Model):
    """Услуги фотографа"""
    name = models.CharField(_("Название"), max_length=100)
    price = models.DecimalField(_("Цена"), max_digits=8, decimal_places=2)
    description = models.TextField(_("Описание"), blank=True)
    is_active = models.BooleanField(_("Активно"), default=True)

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - {self.price}₽"