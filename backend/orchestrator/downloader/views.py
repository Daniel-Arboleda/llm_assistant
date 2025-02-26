import os
import yt_dlp
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Ruta de descarga
DOWNLOAD_PATH = "downloads/audio"

# Asegurarse de que la carpeta de descargas exista
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def get_next_audio_filename():
    """Genera el próximo nombre de archivo de audio."""
    existing_files = [f for f in os.listdir(DOWNLOAD_PATH) if f.startswith("reunion_") and f.endswith(".mp3")]
    existing_numbers = [int(f.split("_")[1].split(".")[0]) for f in existing_files if f.split("_")[1].split(".")[0].isdigit()]
    
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    return f"reunion_{next_number}.mp3"

@csrf_exempt
def download_audio(request):
    """Descarga el audio desde YouTube, lo almacena y lo procesa (transcripción y resumen)."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            youtube_url = data.get("url")

            if not youtube_url:
                return JsonResponse({"error": "No se proporcionó un enlace"}, status=400)

            # Nombre y ruta del archivo de salida
            audio_filename = get_next_audio_filename()
            audio_path = os.path.join(DOWNLOAD_PATH, audio_filename)

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_PATH}/temp_audio.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # Descargar audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            # Verificar si el archivo MP3 se creó correctamente
            final_audio_path = os.path.join(DOWNLOAD_PATH, "temp_audio.mp3")
            if not os.path.exists(final_audio_path):
                return JsonResponse({"error": "Error en la conversión de audio"}, status=500)

            # Renombrar el archivo final
            os.rename(final_audio_path, audio_path)

            print(f"[SUCCESS] Descarga completada y guardada en {audio_path}")

            # Procesar transcripción
            transcript_url = "http://127.0.0.1:8000/transcriber/process_audio/"
            response = requests.post(transcript_url, json={"file_name": audio_filename})

            if response.status_code == 200:
                transcript_data = response.json()
                transcript_file = transcript_data.get("transcript_file", "Transcripción no disponible")
                transcript_path = transcript_data.get("transcript_path", "Ruta no disponible")

                if transcript_file == "Transcripción no disponible" or transcript_path == "Ruta no disponible":
                    return JsonResponse({
                        "message": "Descarga completada, pero la transcripción no está disponible",
                        "audio_file": audio_filename,
                        "transcript_file": transcript_file,
                        "transcript_path": transcript_path
                    })

                print(f"[SUCCESS] Transcripción generada: {transcript_path}")

                # Procesar resumen
                summarization_url = "http://127.0.0.1:8000/summarization/process_transcript/"
                summary_response = requests.post(summarization_url, json={"transcript_file": transcript_file})

                if summary_response.status_code == 200:
                    summary_data = summary_response.json()
                    summary_file = summary_data.get("summary_file", "Resumen no disponible")
                    summary_path = summary_data.get("summary_path", "Ruta no disponible")

                    print(f"[SUCCESS] Resumen generado: {summary_path}")
                    return JsonResponse({
                        "message": "Descarga completada, transcripción y resumen generados correctamente",
                        "audio_file": audio_filename,
                        "transcript_file": transcript_file,
                        "transcript_path": transcript_path,
                        "summary_file": summary_file,
                        "summary_path": summary_path
                    })
                else:
                    return JsonResponse({
                        "message": "Descarga y transcripción completadas, pero hubo un error en la generación del resumen",
                        "audio_file": audio_filename,
                        "transcript_file": transcript_file,
                        "transcript_path": transcript_path,
                        "error": summary_response.text
                    }, status=500)

            else:
                return JsonResponse({"error": f"Error al iniciar la transcripción: {response.text}"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
