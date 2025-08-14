from django import forms
from django.core.mail import send_mail
from django.conf import settings
from core.models import Service

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
        subject = f"Новое сообщение от {self.cleaned_data['name']}"
        message = self.cleaned_data['message']
        from_email = self.cleaned_data['email']
        recipient_list = [settings.DEFAULT_FROM_EMAIL]
        
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

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