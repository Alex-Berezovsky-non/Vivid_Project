from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.conf import settings
import logging
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

from .models import Booking, TimeSlot
from .forms import BookingForm, TimeSlotSelectionForm

def send_telegram_alert(message):
    """
    Отправка уведомления в Telegram с использованием urllib
    """
    TELEGRAM_BOT_API_KEY = getattr(settings, 'TELEGRAM_BOT_API_KEY', None)
    TELEGRAM_USER_ID = getattr(settings, 'TELEGRAM_USER_ID', None)
    
    if not TELEGRAM_BOT_API_KEY or not TELEGRAM_USER_ID:
        logger = logging.getLogger(__name__)
        logger.warning("Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"
    
    data = {
        'chat_id': TELEGRAM_USER_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        # Преобразуем данные в bytes
        data_bytes = urlencode(data).encode('utf-8')
        
        # Создаем запрос
        request = Request(url, data=data_bytes, method='POST')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # Отправляем запрос
        with urlopen(request, timeout=10) as response:
            response_data = response.read().decode('utf-8')
            result = json.loads(response_data)
            
            if result.get('ok'):
                return True
            else:
                logger = logging.getLogger(__name__)
                logger.error(f"Telegram API error: {result.get('description')}")
                return False
                
    except (URLError, HTTPError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка отправки Telegram сообщения: {e}")
        return False
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Неожиданная ошибка: {e}")
        return False

class TimeSlotSelectionView(TemplateView):
    """Выбор даты и доступных слотов времени"""
    template_name = 'bookings/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TimeSlotSelectionForm()
        
        # Получаем дату из GET-параметра, если есть
        selected_date = self.request.GET.get('date')
        if selected_date:
            try:
                from datetime import datetime
                selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                context['selected_date'] = selected_date
                
                # ВРЕМЕННО: только конкретные даты
                available_slots = TimeSlot.objects.filter(
                    date_type='specific',
                    specific_date=selected_date,
                    is_available=True
                )
                
                # Фильтруем полностью занятые слоты
                available_slots = [slot for slot in available_slots if not slot.is_fully_booked()]
                context['available_slots'] = available_slots
                
            except ValueError:
                messages.error(self.request, _("Неверный формат дати"))
        
        return context

class BookingCreateView(CreateView):
    """Создание бронирования"""
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Устанавливаем time_slot ДО обработки запроса
        slot_id = kwargs.get('slot_id')
        self.time_slot = get_object_or_404(TimeSlot, id=slot_id, is_available=True)
        
        # Проверяем доступность слота
        if self.time_slot.is_fully_booked():
            messages.error(request, _("Это временной слот уже занят"))
            return redirect('bookings:calendar')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['time_slot'] = self.time_slot
        return kwargs
    
    def get_initial(self):
        """Устанавливаем начальные значения для формы"""
        initial = super().get_initial()
        # Можно добавить предзаполненные данные, если нужно
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_slot'] = self.time_slot
        return context
    
    def form_valid(self, form):
        # Создаем объект бронирования, но не сохраняем в базу
        booking = form.save(commit=False)
        # Устанавливаем обязательное поле time_slot ПЕРЕД сохранением
        booking.time_slot = self.time_slot
        
        # ВАЛИДАЦИЯ: проверяем, что слот все еще доступен
        if self.time_slot.is_fully_booked():
            messages.error(self.request, _("Это временной слот уже занят"))
            return redirect('bookings:calendar')
        
        # Сохраняем объект в базу
        try:
            booking.save()
        except ValidationError as e:
            # Если есть ошибки валидации, показываем их пользователю
            for error in e.messages:
                messages.error(self.request, error)
            return self.form_invalid(form)
        
        # Сохраняем объект в атрибуте view для дальнейшего использования
        self.object = booking
        
        # Отправляем уведомление в Telegram
        try:
            telegram_msg = (
                f"📅 *Новая запись на съемку!*\n\n"
                f"*Имя:* {booking.client_name}\n"
                f"*Телефон:* `{booking.client_phone}`\n"
                f"*Email:* `{booking.client_email}`\n"
                f"*Тип съемки:* {booking.get_shooting_type_display()}\n"
                f"*Время:* {self.time_slot}\n"
                f"*Код подтверждения:* `{booking.confirmation_code}`\n\n"
                f"*Сообщение:*\n{booking.message[:200]}"
            )
            send_telegram_alert(telegram_msg)
        except Exception as e:
            # Логируем ошибку, но не прерываем выполнение
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка отправки Telegram уведомления: {e}")
        
        messages.success(
            self.request, 
            _("Запись успешно создана! Мы свяжемся с вами для подтверждения.")
        )
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('bookings:booking_done', kwargs={'code': self.object.confirmation_code})

class BookingDoneView(TemplateView):
    """Страница успешного завершения бронирования"""
    template_name = 'bookings/booking_done.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = kwargs.get('code')
        context['booking'] = get_object_or_404(Booking, confirmation_code=code)
        return context

class BookingDetailView(TemplateView):
    """Детальная страница бронирования"""
    template_name = 'bookings/booking_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = kwargs.get('code')
        context['booking'] = get_object_or_404(Booking, confirmation_code=code)
        return context