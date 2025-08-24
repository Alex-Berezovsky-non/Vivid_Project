from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError
import os
from urllib.parse import urlparse, parse_qs

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый формат изображения.')

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.avi', '.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый формат видео.')

class ShootingType(models.Model):
    """Типы съемок (динамические)"""
    name = models.CharField(_("Название типа съемки"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Описание"), blank=True)
    is_active = models.BooleanField(_("Активно"), default=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    
    class Meta:
        verbose_name = _("Тип съемки")
        verbose_name_plural = _("Типы съемок")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Album(models.Model):
    """Альбом фотографий"""
    title = models.CharField(_("Название"), max_length=200)
    slug = models.SlugField(_("URL-адрес"), unique=True)
    description = models.TextField(_("Описание"), blank=True)
    cover = models.ImageField(
        _("Обложка"), 
        upload_to='portfolio/covers/%Y/%m/%d/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    shooting_types = models.ManyToManyField(
        ShootingType,
        verbose_name=_("Типы съемок"),
        blank=True
    )
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    is_featured = models.BooleanField(_("Рекомендуемое"), default=False)
    order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Альбом")
        verbose_name_plural = _("Альбомы")
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:album_detail', kwargs={'slug': self.slug})
    
    def get_shooting_types_display(self):
        # type: ignore 
        types = self.shooting_types.all()
        return ", ".join([st.name for st in types])

class Photo(models.Model):
    """Фотография в альбоме"""
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_("Альбом")
    )
    image = models.ImageField(
        _("Изображение"),
        upload_to='portfolio/photos/%Y/%m/%d/',
        validators=[validate_image_extension]
    )
    title = models.CharField(_("Название"), max_length=200, blank=True)
    description = models.TextField(_("Описание"), blank=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    is_cover_candidate = models.BooleanField(_("Кандидат на обложку"), default=False)

    class Meta:
        verbose_name = _("Фотография")
        verbose_name_plural = _("Фотографии")
        ordering = ['order', 'created_at']

    def __str__(self):
        if self.title:
            return self.title
        return f"Фото {self.pk}"

class Video(models.Model):
    """Видео в портфолио"""
    title = models.CharField(_("Название"), max_length=200)
    video_file = models.FileField(
        _("Видео файл"),
        upload_to='portfolio/videos/%Y/%m/%d/',
        validators=[validate_video_extension],
        blank=True,
        null=True
    )
    youtube_url = models.URLField(_("YouTube ссылка"), blank=True)
    thumbnail = models.ImageField(
        _("Превью"),
        upload_to='portfolio/video_thumbs/%Y/%m/%d/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    description = models.TextField(_("Описание"), blank=True)
    shooting_types = models.ManyToManyField(
        ShootingType,
        verbose_name=_("Типы съемок"),
        blank=True
    )
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Видео")
        verbose_name_plural = _("Видео")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_embed_url(self):
        if not self.youtube_url:
            return None
        
        try:
            # Для ссылок вида: https://www.youtube.com/watch?v=VIDEO_ID
            if 'youtube.com/watch' in self.youtube_url:
                parsed_url = urlparse(self.youtube_url)
                video_id = parse_qs(parsed_url.query).get('v')
                if video_id:
                    return f'https://www.youtube.com/embed/{video_id[0]}'
            
            # Для сокращенных ссылок: https://youtu.be/VIDEO_ID
            elif 'youtu.be' in self.youtube_url:
                parsed_url = urlparse(self.youtube_url)
                video_id = parsed_url.path.strip('/')
                if video_id:
                    return f'https://www.youtube.com/embed/{video_id}'
                    
        except (ValueError, AttributeError, IndexError):
            pass
        
        return None