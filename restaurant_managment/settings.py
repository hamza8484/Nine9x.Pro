import os

from pathlib import Path
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UserConfig',
    'crispy_forms',
    'social_django',
    "configrate",
    "input",
    "purchases",
    "pos",
    "sales",
    "parent",  
    "printsettings",
    "CompanyInfo", 
    "widget_tweaks",  
    "TaxApp", 
    "expense", 
    "support",
    "channels",
    "corsheaders",
    "payments",
    "rest_framework",
    #"employees",
     
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restaurant_managment.middleware.LanguageMiddleware',
]


ROOT_URLCONF = 'restaurant_managment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users', 'templates'),  
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}


# قناة (channel) لأستخدام WebSockets
ASGI_APPLICATION = 'restaurant_managment.asgi.application'

# إعداد Redis (لاستعماله كوسيط للرسائل)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # إذا كنت تستخدم Redis على نفس الجهاز
        },
    },
}
ASGI_APPLICATION = 'configrate.asgi.application'  # تأكد من أن هذا يشير إلى ملف ASGI الصحيح

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # قم بتغيير الرقم 1 إلى رقم قاعدة البيانات المناسب
    }
}



# إعدادات اللغة
LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LANGUAGE_CODE = 'ar'

LANGUAGE_COOKIE_NAME = 'django_language'

USE_I18N = True  # تفعيل الترجمة الدولية
USE_L10N = True  # تفعيل التنسيق المحلي للتواريخ والأرقام
TIME_ZONE = 'UTC'
USE_TZ = True

# المسار الخاص بالترجمات
LOCALE_PATHS = [
    BASE_DIR / 'restaurant_managment' / 'locale',  # مسار مجلد locale داخل مشروعك
]

# باقي إعدادات التطبيق (مثال على WSGI)
WSGI_APPLICATION = 'restaurant_managment.wsgi.application'



# Database


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",  # قاعدة بيانات SQLite
    }
}

# Password validation


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
 
    'django.contrib.auth.backends.ModelBackend',
)


# Static files (CSS, JavaScript, Images)

CRISPY_TEMPLATE_PACK = 'bootstrap4'


STATIC_URL = 'static/'

# تحديد المسار الذي سيتم جمع الملفات فيه عند تنفيذ collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# إذا كنت تستخدم ملفات ثابتة في مجلدات أخرى، يمكنك تحديدها هنا:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'purchases', 'static'),
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = '/'  # أو المسار الذي تريد التوجيه إليه بعد تسجيل الدخول
LOGIN_URL = 'login'  # يجب أن يشير إلى اسم URL الخاص بتسجيل الدخول

# social auth configs for github
SOCIAL_AUTH_GITHUB_KEY = str(os.getenv('GITHUB_KEY'))
SOCIAL_AUTH_GITHUB_SECRET = str(os.getenv('GITHUB_SECRET'))

# لضبط الجلسات والكوكيز:
SESSION_COOKIE_AGE = 3600  # مدة الجلسة ساعة واحدة
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # الجلسة تبقى مفتوحة حتى إغلاق المتصفح إذا لم يكن تم تحديد "تذكرني"
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# إعدادات البريد الإلكتروني في Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hamzajarrar84@gmail.com'  # بريدك الإلكتروني
EMAIL_HOST_PASSWORD = 'Asdf198400'  # كلمة مرور البريد الإلكتروني
