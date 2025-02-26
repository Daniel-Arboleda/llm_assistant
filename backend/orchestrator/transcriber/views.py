import os
import time
import whisper
import logging
import requests
import re
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Configuración de logs
logger = logging.getLogger('transcriber')

# Directorios de almacenamiento
AUDIO_DIR = os.path.abspath(os.path.join(settings.BASE_DIR, "downloads", "audio"))
TRANSCRIPTS_DIR = os.path.abspath(os.path.join(settings.BASE_DIR, "downloads", "transcripts"))

# Asegurar la existencia de las carpetas
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# Lista de formatos de audio soportados
ALLOWED_AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg'}

# Cargar el modelo Whisper solo una vez
model = None

def get_whisper_model():
    global model
    if model is None:
        logger.info("Cargando modelo Whisper...")
        model = whisper.load_model("base")
    return model

def transcribe_audio(file_path):
    """Transcribe un archivo de audio y guarda el resultado."""
    try:
        logger.info(f"Transcribiendo: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Archivo no encontrado: {file_path}")
            return None

        # Verificar la extensión del archivo
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in ALLOWED_AUDIO_EXTENSIONS:
            logger.error(f"Formato de archivo no permitido: {ext}")
            return None

        model = get_whisper_model()
        result = model.transcribe(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{file_name}.txt")

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        return transcript_path

    except Exception as e:
        logger.error(f"Error transcribiendo {file_path}: {e}", exc_info=True)
        return None

@api_view(['POST'])
def process_downloaded_audio(request):
    """Procesa un archivo de audio descargado y lo transcribe, luego envía el texto al summarizer."""
    file_name = request.data.get("file_name")
    if not file_name:
        return Response({"error": "No se proporcionó el nombre del archivo."}, status=400)

    # Validación mejorada del nombre del archivo
    if not re.match(r'^[\w\-. ]+\.[a-zA-Z0-9]+$', file_name):
        logger.error(f"Nombre de archivo inválido: {file_name}")
        return Response({"error": "Nombre de archivo inválido o con caracteres no permitidos."}, status=400)

    file_path = os.path.join(AUDIO_DIR, file_name)
    logger.info(f"Ruta del archivo de audio recibida: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"El archivo no existe: {file_path}")
        return Response({"error": f"El archivo no existe: {file_path}"}, status=404)

    transcript_path = transcribe_audio(file_path)
    if not transcript_path:
        logger.error("Error al transcribir el archivo.")
        return Response({"error": "Error al transcribir el archivo."}, status=500)

    if not os.path.exists(transcript_path):
        logger.error(f"El archivo de transcripción no se creó: {transcript_path}")
        return Response({"error": "No se generó el archivo de transcripción."}, status=500)

    logger.info(f"Archivo de transcripción generado correctamente: {transcript_path}")

    # Enviar la transcripción al servicio de summarization
    summarization_url = "http://127.0.0.1:8000/summarization/process_transcript/"
    logger.info(f"Enviando archivo {os.path.basename(transcript_path)} al servicio de resumen.")

    try:
        response = requests.post(summarization_url, json={"transcript_file": os.path.basename(transcript_path)})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al conectar con el servicio de resumen: {e}", exc_info=True)
        return Response({"error": f"Error al iniciar el resumen: {str(e)}"}, status=500)

    return Response({
        "message": f"Transcripción guardada en {transcript_path}, resumen iniciado.",
        "transcript_file": os.path.basename(transcript_path),
        "transcript_path": transcript_path
    })

@api_view(['POST'])
def manual_transcribe(request):
    """Permite transcribir un archivo de audio manualmente."""
    file_name = request.data.get("file_name")
    if not file_name:
        return Response({"error": "No se proporcionó un nombre de archivo."}, status=400)

    file_path = os.path.abspath(os.path.join(AUDIO_DIR, file_name))
    logger.info(f"Ruta completa del archivo: {file_path}")

    if not os.path.exists(file_path):
        return Response({"error": f"El archivo no existe: {file_path}"}, status=404)

    transcript_path = transcribe_audio(file_path)
    if not transcript_path:
        return Response({"error": "Error al transcribir el archivo."}, status=500)

    return Response({"message": f"Transcripción guardada en {transcript_path}"})

@api_view(['GET'])
def transcriber_status(request):
    """Devuelve el estado del transcriptor verificando la existencia de archivos en la carpeta de transcripciones."""
    try:
        transcripts = os.listdir(TRANSCRIPTS_DIR)
    except FileNotFoundError:
        return Response({"error": "La carpeta de transcripciones no existe."}, status=500)

    return Response({
        "status": "running",
        "transcriptions": transcripts
    })
