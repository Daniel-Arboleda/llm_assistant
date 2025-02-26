import os
import logging
import colorlog
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Definir la carpeta de logs
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe

# Nivel de logging basado en el entorno
LOG_LEVEL = logging.DEBUG if os.getenv("DEBUG", "False") == "True" else logging.INFO

# Configuración del formato de logs con color para consola
LOG_FORMAT = "%(log_color)s[%(levelname)s] %(asctime)s - %(message)s (%(filename)s:%(lineno)d)"
formatter = colorlog.ColoredFormatter(LOG_FORMAT)

# Manejador para la consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Manejador para archivo de logs
file_handler = logging.FileHandler(LOG_DIR / "app.log", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s (%(filename)s:%(lineno)d)"))

# Configuración del logger principal
logger = logging.getLogger("orchestrator")
logger.setLevel(LOG_LEVEL)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Desactivar logs innecesarios de Django
logging.getLogger("django").setLevel(logging.WARNING)

# Mensaje de prueba para verificar que los logs funcionan
logger.info("Sistema de logging configurado correctamente.")
