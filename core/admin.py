from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from core.models import SiteSettings, Service
from core.forms import ServiceForm

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Русификация интерфейса
    verbose_name_plural = _('Настройки сайта')
    
    # Отключаем возможность добавления новых записей
    def has_add_permission(self, request):
        return False
    
    # Отключаем возможность удаления
    def has_delete_permission(self, request, obj=None):
        return False
    
    # Поля для отображения в списке
    list_display = ('title', 'phone', 'email')
    
    # Группировка полей в админке с понятными названиями
    fieldsets = (
        (_('👤 Основная информация'), {
            'fields': ('title', 'phone', 'email', 'address')
        }),
        (_('📝 Тексты'), {
            'fields': ('about_text', 'footer_about', 'copyright_text'),
            'classes': ('wide',),
        }),
        (_('🖼️ Фото фотографа'), {
            'fields': ('photographer_photo', 'photo_preview'),
            'classes': ('wide',),
        }),
        (_('📱 Социальные сети'), {
            'fields': ('instagram', 'telegram', 'whatsapp', 'vk'),
            'classes': ('wide', 'extrapretty'),
            'description': _('Ссылки на социальные сети фотографа')
        }),
    )
    
    readonly_fields = ('photo_preview',)
    
    def photo_preview(self, obj):
        if obj.photographer_photo:
            return mark_safe(f'<img src="{obj.photographer_photo.url}" style="max-height: 300px; max-width: 300px; border-radius: 8px; margin-top: 10px;">')
        return _("Фото не загружено")
    photo_preview.short_description = _("Предпросмотр фото")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    # Русификация интерфейса
    verbose_name = _('Услуга')
    verbose_name_plural = _('Услуги')
    
    # Кастомные методы для отображения
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_description.short_description = _('Описание')
    
    def price_display(self, obj):
        return f"{obj.price} ₽"
    price_display.short_description = _('Цена')
    
    # Настройки отображения списка
    list_display = ('name', 'price_display', 'is_active', 'short_description')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('price',)
    
    # Группировка полей при редактировании
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'is_active')
        }),
        (_('Подробное описание'), {
            'fields': ('description',),
            'classes': ('wide',),
        }),
    )