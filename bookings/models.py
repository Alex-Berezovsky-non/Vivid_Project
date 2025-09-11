from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

class TimeSlot(models.Model):
    """Модель для хранения доступных слотов времени"""
    
    DATE_CHOICES = [
        ('weekday', 'Будний день (Пн-Пт)'),
        ('weekend', 'Выходной (Сб-Вс)'),
        ('specific', 'Конкретная дата'),
    ]
    
    date_type = models.CharField(
        _("Тип даты"),
        max_length=10,
        choices=DATE_CHOICES,
        default='specific'
    )
    
    specific_date = models.DateField(
        _("Конкретная дата"),
        null=True,
        blank=True
    )
    
    start_time = models.TimeField(_("Время начала"))
    end_time = models.TimeField(_("Время окончания"))
    is_available = models.BooleanField(_("Доступен"), default=True)
    max_bookings = models.PositiveIntegerField(
        _("Максимум записей"),
        default=1,
        help_text=_("Максимальное количество броней на этот слот")
    )
    
    class Meta:
        verbose_name = _("Временной слот")
        verbose_name_plural = _("Временные слоты")
        ordering = ['specific_date', 'start_time']
    
    def __str__(self):
        if self.date_type == 'specific' and self.specific_date:
            return f"{self.specific_date} {self.start_time}-{self.end_time}"
        elif self.date_type == 'weekday':
            return f"Будни {self.start_time}-{self.end_time}"
        else:
            return f"Выходные {self.start_time}-{self.end_time}"
    
    def get_available_slots(self):
        """Получить количество оставшихся мест"""
        booked_count = self.bookings.filter(is_confirmed=True).count()
        return self.max_bookings - booked_count
    
    def is_fully_booked(self):
        """Проверить, полностью ли занят слот"""
        return self.get_available_slots() <= 0
    
    def clean(self):
        """Валидация данных"""
        if self.date_type == 'specific' and not self.specific_date:
            raise ValidationError(_("Для конкретной даты необходимо указать дату"))
        
        # ПРОВЕРКА НА None ДЛЯ ВРЕМЕНИ
        if self.start_time is None or self.end_time is None:
            raise ValidationError(_("Время начала и окончания должны быть указаны"))
        
        # ТЕПЕРЬ МОЖНО БЕЗОПАСНО СРАВНИВАТЬ
        if self.start_time >= self.end_time:
            raise ValidationError(_("Время начала должно быть раньше времени окончания"))
        
        # ПРОВЕРКА ДАТЫ
        if (self.date_type == 'specific' and 
            self.specific_date is not None and
            self.specific_date < timezone.now().date()):
            raise ValidationError(_("Нельзя создавать слоты на прошедшие даты"))

class Booking(models.Model):
    """Модель бронирования"""
    
    SHOOTING_TYPES = [
        ('portrait', 'Портретная съемка'),
        ('lovestory', 'Love Story'),
        ('family', 'Семейная фотосессия'),
        ('other', 'Другое'),
    ]
    
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_("Временной слот")
    )
    
    # Информация о клиенте
    client_name = models.CharField(_("Имя клиента"), max_length=100)
    client_email = models.EmailField(_("Email клиента"))
    client_phone = models.CharField(_("Телефон клиента"), max_length=20)
    shooting_type = models.CharField(
        _("Тип съемки"),
        max_length=20,
        choices=SHOOTING_TYPES,
        default='portrait'
    )
    message = models.TextField(_("Дополнительная информация"), blank=True)
    
    # Статус брони
    is_confirmed = models.BooleanField(_("Подтверждено"), default=False)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    confirmation_code = models.CharField(
        _("Код подтверждения"),
        max_length=20,
        unique=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _("Бронь")
        verbose_name_plural = _("Брони")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.time_slot}"
    
    def save(self, *args, **kwargs):
        """Генерация кода подтверждения при создании"""
        if not self.confirmation_code:
            import uuid
            self.confirmation_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('bookings:booking_detail', kwargs={'code': self.confirmation_code})