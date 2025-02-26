import time
import logging
from django.db import models
from django.apps import apps


logger = logging.getLogger(__name__)

start_time = time.time()

# Obtener el nombre de la aplicación de forma dinámica
app_name = apps.get_containing_app_config(__name__).name

# Aquí puedes definir tus modelos normalmente

elapsed_time = time.time() - start_time
logger.info(f'Modelo de {app_name} cargado en {elapsed_time:.4f} segundos')
