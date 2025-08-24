import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки для разработки (не для production)
SECRET_KEY = os.getenv("SECRET_KEY")  # Секретный ключ из переменных окружения
DEBUG = True  # Режим отладки
ALLOWED_HOSTS = []  # Разрешенные хосты

# Список установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',          # Админ-панель
    'django.contrib.auth',           # Аутентификация
    'django.contrib.contenttypes',   # Система типов контента
    'django.contrib.sessions',       # Сессии
    'django.contrib.messages',       # Сообщения
    'django.contrib.staticfiles',    # Статические файлы
    'core.apps.CoreConfig',          # Основное приложение
    'django_filters',                # Фильтрация данных
    'portfolio.apps.PortfolioConfig' # Приложение портфолио
]

# Промежуточное ПО (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware', # Сессии
    'django.middleware.common.CommonMiddleware',           # Общие функции
    'django.middleware.csrf.CsrfViewMiddleware',           # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware', # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от clickjacking
]

# Корневая конфигурация URL
ROOT_URLCONF = 'framed.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Директории с шаблонами
        'APP_DIRS': True,  # Поиск шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [  # Контекстные процессоры
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'framed.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок БД
        'NAME': BASE_DIR / 'db.sqlite3',        # Путь к файлу БД
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Проверка схожести с атрибутами пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Минимальная длина
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Проверка на распространенные пароли
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Проверка на чисто числовой пароль
    },
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'         # Язык по умолчанию
TIME_ZONE = 'Europe/Moscow'     # Часовой пояс
USE_I18N = True                 # Включение интернационализации
USE_L10N = True                 # Включение локализации
USE_TZ = True                   # Использование временных зон

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'  # URL-префикс для статических файлов
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Дополнительные директории со статическими файлами
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Директория для collectstatic

# Медиа файлы (загружаемые пользователями)
MEDIA_URL = '/media/'   # URL-префикс для медиа файлов
MEDIA_ROOT = BASE_DIR / 'media'  # Директория для хранения медиа файлов

# Тип поля первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Email Settings (Yandex)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('YANDEX_EMAIL')  # alex-berez.24-17@yandex.ru
EMAIL_HOST_PASSWORD = os.getenv('YANDEX_EMAIL_PASSWORD')  # pckirxfkqgbldcnz
DEFAULT_FROM_EMAIL = os.getenv('YANDEX_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # Для админ-уведомлений
# Telegram
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
BASE_URL = os.getenv("BASE_URL")