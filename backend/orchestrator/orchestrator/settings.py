import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configuración del logger
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_DIR / "settings.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

start_time = time.time()
logger.info("Inicio de carga de settings.py")

# Cargar variables de entorno
section_start = time.time()
load_dotenv()
logger.info("Variables de entorno cargadas en %.2f segundos." % (time.time() - section_start))

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración sensible desde el .env
section_start = time.time()
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "clave_por_defecto")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
logger.info("Configuración básica cargada en %.2f segundos." % (time.time() - section_start))

# Cargar modelo de IA y claves API
section_start = time.time()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    logger.warning("No se encontró MODEL_PATH en las variables de entorno.")
logger.info("Configuración de API y modelo cargada en %.2f segundos." % (time.time() - section_start))

# Configuración de Logging
section_start = time.time()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s - %(message)s (%(filename)s:%(lineno)d)',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'formatter': 'verbose',
        },
        'transcriber_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'transcriber.log'),
            'formatter': 'verbose',
        },
        'summarization_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'summarization.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'transcriber': {
            'handlers': ['transcriber_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'summarization': {
            'handlers': ['summarization_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
logger.info("Sistema de logging configurado en %.2f segundos." % (time.time() - section_start))

# Configuración de base de datos
section_start = time.time()
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
        'USER': os.getenv("DB_USER", ""),
        'PASSWORD': os.getenv("DB_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", ""),
        'PORT': os.getenv("DB_PORT", ""),
    }
}
logger.info("Configuración de base de datos cargada en %.2f segundos." % (time.time() - section_start))

# Aplicaciones instaladas
section_start = time.time()
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'api',
    'downloader',
    'transcriber',
    'summarization',
    'report',
    'rag',
]
logger.info("Aplicaciones instaladas cargadas en %.2f segundos." % (time.time() - section_start))

# Registro de carga de apps 
INSTALLED_APPS_LOGGING = {}

for app in INSTALLED_APPS:
    start_time = time.time()
    try:
        __import__(app)  # Intenta importar cada app manualmente
    except Exception as e:
        logger.error(f"Error al cargar {app}: {e}")
    finally:
        elapsed_time = time.time() - start_time
        INSTALLED_APPS_LOGGING[app] = elapsed_time
        logger.info(f"Aplicación {app} cargada en {elapsed_time:.3f} segundos")

# Registro de carga de modelos
for app in INSTALLED_APPS:
    try:
        logger.info(f"Modelo de {app} cargado en {INSTALLED_APPS_LOGGING.get(app, 0):.4f} segundos")
    except Exception as e:
        logger.error(f"Error al registrar el modelo de {app}: {e}")

# Middleware
section_start = time.time()
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
logger.info("Middleware cargado en %.2f segundos." % (time.time() - section_start))

# Configuración de URLs
ROOT_URLCONF = 'orchestrator.urls'

# Configuración de plantillas
section_start = time.time()
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
logger.info("Configuración de plantillas cargada en %.2f segundos." % (time.time() - section_start))

WSGI_APPLICATION = 'orchestrator.wsgi.application'

# Validadores de contraseña
section_start = time.time()
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
logger.info("Validadores de contraseña cargados en %.2f segundos." % (time.time() - section_start))

# Configuración de internacionalización
section_start = time.time()
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
logger.info("Configuración de internacionalización cargada en %.2f segundos." % (time.time() - section_start))

# Configuración de archivos estáticos
section_start = time.time()
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
logger.info("Configuración de archivos estáticos cargada en %.2f segundos." % (time.time() - section_start))

# Registro final de tiempo
logger.info("Configuración de Django cargada completamente en %.2f segundos." % (time.time() - start_time))
