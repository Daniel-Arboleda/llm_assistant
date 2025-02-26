import time
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class SummarizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summarization'

    def ready(self):
        start_time = time.time()
        super().ready()
        elapsed_time = time.time() - start_time
        logger.info(f'App {self.name} cargada en {elapsed_time:.4f} segundos')
