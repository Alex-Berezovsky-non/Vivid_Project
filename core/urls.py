from django.urls import path
from .views import (
    HomeView,
    AboutView,
    ServicesView,
    ContactView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('contacts/', ContactView.as_view(), name='contacts'),
]