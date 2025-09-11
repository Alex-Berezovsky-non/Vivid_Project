from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import TimeSlot, Booking
from .filters import DateTypeFilter  # Импортируем наш фильтр

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Админка для временных слотов с русской локализацией"""
    
    # Заголовки в админке
    verbose_name = _("Временной слот")
    verbose_name_plural = _("Временные слоты")
    
    # Отображение в списке
    list_display = [
        'format_date_display', 
        'format_time_display', 
        'availability_status',
        'bookings_count',
        'max_bookings'
    ]
    
    list_editable = ['max_bookings']
    list_filter = [
        DateTypeFilter,  # Используем наш кастомный фильтр
        'is_available', 
        'specific_date'
    ]
    
    search_fields = ['specific_date']
    ordering = ['specific_date', 'start_time']
    
    # Группировка полей при редактировании
    fieldsets = (
        (_('Основные настройки'), {
            'fields': (
                'date_type', 
                'specific_date',
                'start_time', 
                'end_time'
            )
        }),
        (_('Доступность и лимиты'), {
            'fields': (
                'is_available',
                'max_bookings'
            ),
            'classes': ('wide',),
        }),
        (_('Статистика'), {
            'fields': ('bookings_count_display',),
            'classes': ('collapse',),
        }),
    )
    
    # Кастомные методы для отображения
    def format_date_display(self, obj):
        """Форматирование даты для отображения"""
        if obj.date_type == 'specific' and obj.specific_date:
            return obj.specific_date.strftime('%d.%m.%Y')
        elif obj.date_type == 'weekday':
            return "Будние дни"
        else:
            return "Выходные дни"
    format_date_display.short_description = _('Дата')
    format_date_display.admin_order_field = 'specific_date'
    
    def format_time_display(self, obj):
        """Форматирование времени для отображения"""
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    format_time_display.short_description = _('Время')
    
    def availability_status(self, obj):
        """Статус доступности с цветом"""
        if obj.is_available:
            if obj.get_available_slots() > 0:
                return mark_safe('<span style="color: green;">✅ Доступен</span>')
            else:
                return mark_safe('<span style="color: orange;">⚠️ Занят</span>')
        else:
            return mark_safe('<span style="color: red;">❌ Недоступен</span>')
    availability_status.short_description = _('Статус')
    
    def bookings_count(self, obj):
        """Количество броней и свободных мест"""
        booked = obj.bookings.filter(is_confirmed=True).count()
        free = obj.get_available_slots()
        return f"{booked}/{obj.max_bookings} (свободно: {free})"
    bookings_count.short_description = _('Брони')
    
    def bookings_count_display(self, obj):
        """Отображение статистики броней (только для чтения)"""
        booked = obj.bookings.filter(is_confirmed=True).count()
        free = obj.get_available_slots()
        return f"Забронировано: {booked} из {obj.max_bookings}, Свободно: {free}"
    bookings_count_display.short_description = _('Статистика броней')
    
    # Поле только для чтения
    readonly_fields = ['bookings_count_display']
    
    # Действия для админки
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        """Действие: сделать выбранные слоты доступными"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} слотов стало доступными")
    make_available.short_description = _('Сделать выбранные слоты доступными')
    
    def make_unavailable(self, request, queryset):
        """Действие: сделать выбранные слоты недоступными"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} слотов стало недоступными")
    make_unavailable.short_description = _('Сделать выбранные слоты недоступными')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Админка для бронирований с русской локализацией"""
    
    # Заголовки в админке
    verbose_name = _("Бронирование")
    verbose_name_plural = _("Бронирования")
    
    # Отображение в списке
    list_display = [
        'client_name',
        'contact_info',
        'shooting_type_display',
        'time_slot_link',
        'status_badge',
        'is_confirmed',  # Реальное поле для редактирования
        'created_date'
    ]
    
    list_editable = ['is_confirmed']  # Редактируем реальное поле
    list_filter = [
        'is_confirmed',
        'shooting_type',
        ('created_at', admin.DateFieldListFilter),
        'time_slot__specific_date'
    ]
    
    search_fields = [
        'client_name', 
        'client_email', 
        'client_phone', 
        'confirmation_code'
    ]
    
    readonly_fields = [
        'created_at', 
        'confirmation_code',
        'booking_details',
        'status_badge_display'
    ]
    
    ordering = ['-created_at']
    
    # Группировка полей при редактировании
    fieldsets = (
        (_('Контактная информация'), {
            'fields': (
                'client_name', 
                'client_email', 
                'client_phone'
            ),
            'classes': ('wide',),
        }),
        (_('Детали фотосессии'), {
            'fields': (
                'time_slot',
                'shooting_type',
                'message'
            )
        }),
        (_('Статус и подтверждение'), {
            'fields': (
                'is_confirmed',  # Реальное поле для редактирования
                'status_badge_display',  # Только для просмотра
                'confirmation_code',
                'booking_details'
            ),
            'classes': ('collapse',),
        }),
        (_('Системная информация'), {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    # Кастомные методы для отображения
    def contact_info(self, obj):
        """Контактная информация в компактном виде"""
        return f"{obj.client_phone} | {obj.client_email}"
    contact_info.short_description = _('Контакты')
    
    def shooting_type_display(self, obj):
        """Отображение типа съемки с иконкой"""
        icons = {
            'portrait': '📷',
            'lovestory': '💕',
            'family': '👨‍👩‍👧‍👦',
            'other': '❓'
        }
        return f"{icons.get(obj.shooting_type, '')} {obj.get_shooting_type_display()}"
    shooting_type_display.short_description = _('Тип съемки')
    
    def time_slot_link(self, obj):
        """Ссылка на временной слот"""
        url = reverse('admin:bookings_timeslot_change', args=[obj.time_slot.id])
        return mark_safe(f'<a href="{url}">{obj.time_slot}</a>')
    time_slot_link.short_description = _('Временной слот')
    
    def status_badge(self, obj):
        """Статус брони с цветным бейджем"""
        if obj.is_confirmed:
            return mark_safe('<span style="color: green; font-weight: bold;">✅ Подтверждено</span>')
        else:
            return mark_safe('<span style="color: orange; font-weight: bold;">⏳ Ожидает</span>')
    status_badge.short_description = _('Статус')
    status_badge.allow_tags = True
    
    def status_badge_display(self, obj):
        """Статус брони для формы редактирования (только чтение)"""
        return self.status_badge(obj)
    status_badge_display.short_description = _('Текущий статус')
    status_badge_display.allow_tags = True
    
    def created_date(self, obj):
        """Дата создания в удобном формате"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_date.short_description = _('Создано')
    created_date.admin_order_field = 'created_at'
    
    def booking_details(self, obj):
        """Детальная информация о брони (только для чтения)"""
        details = [
            f"<strong>Код подтверждения:</strong> {obj.confirmation_code}",
            f"<strong>Создано:</strong> {obj.created_at.strftime('%d.%m.%Y %H:%M')}",
            f"<strong>Время съемки:</strong> {obj.time_slot}",
            f"<strong>Статус:</strong> {'Подтверждено' if obj.is_confirmed else 'Ожидает подтверждения'}"
        ]
        return mark_safe('<br>'.join(details))
    booking_details.short_description = _('Информация о брони')
    
    # Действия для админки
    actions = ['confirm_bookings', 'unconfirm_bookings', 'export_contacts']
    
    def confirm_bookings(self, request, queryset):
        """Подтвердить выбранные брони"""
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f"{updated} броней подтверждено")
    confirm_bookings.short_description = _('Подтвердить выбранные брони')
    
    def unconfirm_bookings(self, request, queryset):
        """Снять подтверждение с выбранных броней"""
        updated = queryset.update(is_confirmed=False)
        self.message_user(request, f"{updated} броней ожидают подтверждения")
    unconfirm_bookings.short_description = _('Снять подтверждение с броней')
    
    def export_contacts(self, request, queryset):
        """Экспорт контактов (заглушка для примера)"""
        self.message_user(request, "Экспорт контактов будет реализован в будущем")
    export_contacts.short_description = _('Экспорт контактов выбранных броней')
    
    # Настройка отображения формы
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Делаем поле времени только для чтения при редактировании
        if obj:
            form.base_fields['time_slot'].disabled = True
        return form

# Кастомизация заголовков админки
admin.site.site_header = _("Панель управления фотографом")
admin.site.site_title = _("Администрирование бронирований")
admin.site.index_title = _("Управление записями на фотосессии")