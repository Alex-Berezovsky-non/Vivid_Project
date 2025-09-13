from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review,SocialReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'email', 'rating', 'text', 'photo']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ваше имя')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': _('Ваш email')
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'choices': [(i, str(i)) for i in range(1, 6)]  
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Расскажите о вашем опыте...'),
                'rows': 4
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'author': _('Ваше имя'),
            'email': _('Email'),
            'rating': _('Оценка'),
            'text': _('Текст отзыва'),
            'photo': _('Фото (необязательно)'),
        }

class SocialReviewForm(forms.ModelForm):
    class Meta:
        model = SocialReview
        fields = ['source', 'external_id', 'author', 'text', 'rating', 'photo_url', 'post_url', 'created_at']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': 3})
        }