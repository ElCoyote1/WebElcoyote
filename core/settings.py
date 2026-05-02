import os  # <-- Importante para leer variables de entorno
from pathlib import Path
import dj_database_url # <-- Esto lo vamos a necesitar para la base de datos de Render

BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: En Render la clave se saca de una variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure--7zz*^sov_g8vyp=vq21eiis5&q5=c@xsb!(izwmn&3dx)h=g!')

# DEBUG: En Render debe ser False para que sea seguro
DEBUG = 'RENDER' not in os.environ

# ALLOWED_HOSTS: Permitimos localhost y el dominio que te de Render
ALLOWED_HOSTS = []
render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)
else:
    ALLOWED_HOSTS.append("127.0.0.1")
    ALLOWED_HOSTS.append("localhost")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'servicios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- AGREGAR ESTO para los archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Agregado por seguridad
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# BASE DE DATOS: Configuración inteligente para Render
# Si estás en Render usa PostgreSQL, si no, usa SQLite (tu db actual)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# ESTATICOS: Muy importante para que el mapa y el Coyote se vean en Render
STATIC_URL = 'static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'