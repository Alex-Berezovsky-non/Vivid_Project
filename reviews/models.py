from django.db import models
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'), 
        ('rejected', 'Отклонено')
    ]
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    author = models.CharField(_("Имя автора"), max_length=100)
    email = models.EmailField(_("Email"))
    rating = models.PositiveIntegerField(_("Оценка (1-5)"), choices=RATING_CHOICES)
    text = models.TextField(_("Текст отзыва"))
    photo = models.ImageField(_("Фото"), upload_to='reviews/', blank=True, null=True)
    is_public = models.BooleanField(_("Публичный"), default=False)
    status = models.CharField(_("Статус"), max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author} - {self.rating}★"

class SocialReview(models.Model):
    SOURCE_CHOICES = [
        ('instagram', 'Instagram'),
        ('vk', 'VKontakte'),
    ]
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    source = models.CharField(_("Источник"), max_length=20, choices=SOURCE_CHOICES)
    external_id = models.CharField(_("ID в соцсети"), max_length=100, unique=True)
    author = models.CharField(_("Автор"), max_length=100)
    text = models.TextField(_("Текст"))
    rating = models.PositiveIntegerField(_("Оценка (1-5)"), choices=RATING_CHOICES)
    photo_url = models.URLField(_("Ссылка на фото"), blank=True)
    post_url = models.URLField(_("Ссылка на пост"))
    created_at = models.DateTimeField(_("Дата создания в соцсети"))
    imported_at = models.DateTimeField(_("Дата импорта"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Социальный отзыв")
        verbose_name_plural = _("Социальные отзывы")
        ordering = ['-created_at']