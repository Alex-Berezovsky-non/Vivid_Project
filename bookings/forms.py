from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking, TimeSlot
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    """Форма для создания бронирования"""
    
    class Meta:
        model = Booking
        fields = [
            'client_name', 
            'client_email', 
            'client_phone',
            'shooting_type', 
            'message'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ваше полное имя')
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ваш email')
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('+7 (999) 999-99-99')
            }),
            'shooting_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Расскажите о ваших пожеланиях...'),
                'rows': 4
            }),
        }
        labels = {
            'client_name': _('Ваше имя'),
            'client_email': _('Email'),
            'client_phone': _('Телефон'),
            'shooting_type': _('Тип съемки'),
            'message': _('Дополнительная информация'),
        }
    
    def __init__(self, *args, **kwargs):
        self.time_slot = kwargs.pop('time_slot', None)
        super().__init__(*args, **kwargs)

class TimeSlotSelectionForm(forms.Form):
    """Форма для выбора временного слота"""
    
    date = forms.DateField(
        label=_("Дата съемки"),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': '',  # Будет установлено через JS
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.utils import timezone
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        self.fields['date'].widget.attrs['min'] = tomorrow.isoformat()