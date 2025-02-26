import torch
import time
import logging
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Configuración de logs
logger = logging.getLogger(__name__)

# Variables globales para el modelo
whisper_model = None
whisper_processor = None

def load_whisper():
    """Carga el modelo Whisper solo cuando sea necesario y mide el tiempo de carga."""
    global whisper_model, whisper_processor

    if whisper_model is None or whisper_processor is None:
        logger.info("🚀 Cargando modelo Whisper en memoria...")
        start_time = time.time()

        device = "cuda" if torch.cuda.is_available() else "cpu"

        try:
            whisper_model = WhisperForConditionalGeneration.from_pretrained(
                "openai/whisper-large"
            ).to(device)
            whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-large")

            load_time = time.time() - start_time
            logger.info(f"✅ Modelo Whisper cargado en {load_time:.2f} segundos.")

            if load_time > 10:  # Si tarda más de 10 segundos, mostrar advertencia
                logger.warning("⚠️ El modelo Whisper tardó más de 10 segundos en cargarse.")

        except Exception as e:
            logger.error(f"❌ Error al cargar el modelo Whisper: {e}")
            whisper_model = None
            whisper_processor = None

    return whisper_model, whisper_processor

def unload_whisper():
    """Libera memoria descargando el modelo."""
    global whisper_model, whisper_processor
    if whisper_model is not None:
        del whisper_model
        del whisper_processor
        torch.cuda.empty_cache()  # Libera la memoria en GPU
        logger.info("♻️ Whisper descargado de la memoria.")
    whisper_model = None
    whisper_processor = None
