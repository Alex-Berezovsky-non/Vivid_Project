from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import ShootingType, Album, Photo, Video

@admin.register(ShootingType)
class ShootingTypeAdmin(admin.ModelAdmin):
    """Админка для типов съемок"""
    list_display = ['name', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']  
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'is_active', 'order')
        }),
        (_('Описание'), {
            'fields': ('description',),
            'classes': ('wide',)
        }),
    )


class PhotoInline(admin.TabularInline):
    """Фотографии внутри альбома"""
    model = Photo
    extra = 1
    fields = ['image', 'title', 'order', 'is_cover_candidate', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 150px;">')
        return _("Нет изображения")
    image_preview.short_description = _("Предпросмотр")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Админка для альбомов"""
    list_display = ['title', 'cover_preview', 'shooting_types_list', 'is_published', 'is_featured', 'order', 'created_at']
    list_editable = ['is_published', 'is_featured', 'order']
    list_filter = ['is_published', 'is_featured', 'shooting_types']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['shooting_types']
    inlines = [PhotoInline]
    readonly_fields = ['cover_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'slug', 'cover', 'cover_preview')
        }),
        (_('Настройки'), {
            'fields': ('shooting_types', 'is_published', 'is_featured', 'order')
        }),
        (_('Описание'), {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        (_('Даты'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_preview(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" style="max-height: 200px; max-width: 300px;">')
        return _("Нет обложки")
    cover_preview.short_description = _("Предпросмотр обложки")
    
    def shooting_types_list(self, obj):
        return ", ".join([st.name for st in obj.shooting_types.all()])
    shooting_types_list.short_description = _("Типы съемок")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Админка для фотографий"""
    list_display = ['title', 'album', 'image_preview', 'order', 'is_cover_candidate', 'created_at']
    list_editable = ['order', 'is_cover_candidate']
    list_filter = ['album', 'is_cover_candidate']
    search_fields = ['title', 'description', 'album__title']
    readonly_fields = ['image_preview', 'created_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('album', 'image', 'image_preview')
        }),
        (_('Детали'), {
            'fields': ('title', 'description', 'order', 'is_cover_candidate')
        }),
        (_('Дата создания'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 150px;">')
        return _("Нет изображения")
    image_preview.short_description = _("Предпросмотр")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Админка для видео"""
    list_display = ['title', 'video_type', 'is_published', 'created_at']
    list_editable = ['is_published']
    list_filter = ['is_published', 'shooting_types']
    search_fields = ['title', 'description']
    filter_horizontal = ['shooting_types']
    readonly_fields = ['thumbnail_preview', 'created_at', 'embed_preview']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'is_published')
        }),
        (_('Видео контент'), {
            'fields': ('video_file', 'youtube_url', 'thumbnail', 'thumbnail_preview')
        }),
        (_('Детали'), {
            'fields': ('description', 'shooting_types')
        }),
        (_('Предпросмотр'), {
            'fields': ('embed_preview',),
            'classes': ('wide',)
        }),
        (_('Дата создания'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-height: 100px; max-width: 150px;">')
        return _("Нет превью")
    thumbnail_preview.short_description = _("Предпросмотр превью")
    
    def embed_preview(self, obj):
        if obj.get_embed_url():
            return mark_safe(f'<iframe src="{obj.get_embed_url()}" width="300" height="200" frameborder="0" allowfullscreen></iframe>')
        elif obj.video_file:
            return mark_safe(f'<video width="300" height="200" controls><source src="{obj.video_file.url}">Ваш браузер не поддерживает видео</video>')
        return _("Нет видео для предпросмотра")
    embed_preview.short_description = _("Предпросмотр видео")
    
    def video_type(self, obj):
        if obj.youtube_url:
            return "YouTube"
        elif obj.video_file:
            return "Файл"
        return "Не указано"
    video_type.short_description = _("Тип видео")


# Настройка заголовков админки
admin.site.site_header = _("Панель управления фотографом")
admin.site.site_title = _("Администрирование сайта")
admin.site.index_title = _("Добро пожаловать в панель управления")