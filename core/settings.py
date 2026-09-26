from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Segurança ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-fallback-dev-only")
DEBUG      = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# ─── Apps ─────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Cloudinary ANTES do staticfiles ← obrigatório
    'cloudinary',
    'cloudinary_storage',
    "django.contrib.staticfiles",
    # Terceiros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # Meus apps
    'users',
    'posts',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.debug',
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ─── Banco de dados ───────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─── Auth ─────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Internacionalização ──────────────────────────────────────────────────────
LANGUAGE_CODE = "pt-br"
TIME_ZONE     = "America/Sao_Paulo"
USE_I18N      = True
USE_TZ        = True

# ─── Arquivos estáticos e de mídia ───────────────────────────────────────────
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL   = "/media/"
MEDIA_ROOT  = BASE_DIR / "media"

# ─── Cloudinary ───────────────────────────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY':    os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

import cloudinary
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    api_key    = os.environ.get('CLOUDINARY_API_KEY', ''),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', ''),
)

if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    # Produção: usa Cloudinary para mídia e Whitenoise para estáticos
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # Desenvolvimento local
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# ─── REST Framework ───────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# ─── JWT ──────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
    'AUTH_HEADER_TYPES':      ('Bearer',),
}

# ─── CORS ─────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

VERCEL_URL = os.environ.get("VERCEL_URL")
if VERCEL_URL:
    CORS_ALLOWED_ORIGINS.append(VERCEL_URL)

# ─── CSRF ─────────────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-86c3a.up.railway.app',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'