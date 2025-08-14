from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель
    path('', include('core.urls')),  #  URL core-приложения
]