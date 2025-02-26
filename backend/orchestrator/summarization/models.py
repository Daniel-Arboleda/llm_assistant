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









# import os
# import time
# import logging
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from django.apps import apps

# logger = logging.getLogger(__name__)

# # Asegurar que la ruta del modelo está disponible
# MODEL_PATH = os.getenv("MODEL_PATH")

# if not os.path.exists(MODEL_PATH):
#     raise ValueError(f"La ruta del modelo '{MODEL_PATH}' no está definida, no existe o es incorrecta. Asegúrate de configurar el archivo .env correctamente.")

# try:
#     total_start_time = time.time()
#     start_time = time.time()

#     # Obtener el nombre de la aplicación de forma dinámica
#     app_name = apps.get_containing_app_config(__name__).name
#     logger.info(f"Iniciando carga del modelo para {app_name}...")
    
#     model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
#     elapsed_time = time.time() - start_time
#     logger.info(f"Modelo cargado en {elapsed_time:.4f} segundos.")

#     start_time = time.time()
#     tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
#     elapsed_time = time.time() - start_time
#     logger.info(f"Tokenizador cargado en {elapsed_time:.4f} segundos.")

#     elapsed_time = time.time() - start_time
#     logger.info(f'Modelo de {app_name} cargado en {elapsed_time:.4f} segundos')

#     total_elapsed_time = time.time() - total_start_time
#     logger.info(f"Tiempo total de carga del modelo: {total_elapsed_time:.4f} segundos.")

# except Exception as e:
#     raise ValueError(f"Error al cargar el modelo desde {MODEL_PATH}: {str(e)}")
# import os
# import time
# import torch
# import gc
# import psutil
# import platform
# from dotenv import load_dotenv
# from transformers import AutoModelForCausalLM, AutoTokenizer

# load_dotenv()  # Cargar variables desde .env

# # 📌 Ruta del modelo descargado
# MODEL_PATH = os.getenv("MODEL_PATH")
# if MODEL_PATH is None:
#     raise ValueError("\u274c ERROR: La variable de entorno MODEL_PATH no está definida.")

# # 📌 Configuración de memoria
# MAX_GPU_MEMORY = float(os.getenv("MAX_GPU_MEMORY", 0.8))  # 80% de la memoria GPU
# MAX_RAM_MEMORY = float(os.getenv("MAX_RAM_MEMORY", 0.8))  # 80% de la RAM

# start_time = time.time()
# print("🚀 Cargando modelo para validación...".encode("utf-8", "ignore").decode("utf-8"))


# try:
#     # 📌 Detección de GPU y selección dinámica
#     if torch.cuda.is_available():
#         num_gpus = torch.cuda.device_count()
#         device = "cuda"
#         selected_gpu = 0  # Selecciona la GPU 0 por defecto
#         gpu_name = torch.cuda.get_device_name(selected_gpu)
#         print(f"✅ GPU detectada: {gpu_name} ({num_gpus} disponibles)".encode("utf-8", "ignore").decode("utf-8"))

#         # Configuración dinámica de memoria por GPU en bytes
#         max_memory_config = {
#             i: int(MAX_GPU_MEMORY * torch.cuda.get_device_properties(i).total_memory)
#             for i in range(num_gpus)
#         }

#         torch_dtype = torch.float16  # Usar menor precisión en GPU para mejor rendimiento
#     else:
#         device = "cpu"
#         gpu_name = "Ninguna"
#         max_memory_config = None
#         torch_dtype = torch.float32  # Mantener precisión en CPU
#         print("⚠️ No se detectó GPU. Usando CPU.".encode("utf-8", "ignore").decode("utf-8"))

#     # 📌 Liberar caché antes de cargar el modelo (evita Out of Memory)
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
#         gc.collect()
#         print("✅ Caché de GPU limpiada antes de cargar el modelo.".encode("utf-8", "ignore").decode("utf-8"))

#     model_load_start = time.time()

#     # 📌 Cargar modelo y tokenizer con configuración ajustada
#     try:
#         model = AutoModelForCausalLM.from_pretrained(
#             MODEL_PATH,
#             torch_dtype=torch_dtype,
#             device_map="auto" if device == "cuda" else None,
#             **({"max_memory": max_memory_config} if device == "cuda" else {})
#         )
#         tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
#     except OSError as e:
#         raise RuntimeError(f"❌ Error al cargar el modelo desde {MODEL_PATH}: {e}")
#     except RuntimeError as e:
#         raise RuntimeError(f"❌ Error de memoria al cargar el modelo: {e}")

#     model.to(device)
#     model_load_end = time.time()
    
#     print(f"✅ Modelo cargado en {model_load_end - model_load_start:.2f} segundos en {device.upper()} ({gpu_name})".encode("utf-8", "ignore").decode("utf-8"))

#     # 📌 Prueba de inferencia
#     input_text = "¿Cómo funciona un modelo de lenguaje?"
#     inputs = tokenizer(input_text, return_tensors="pt").to(device)

#     inference_start = time.time()
#     print("🔍 Generando respuesta...".encode("utf-8", "ignore").decode("utf-8"))
#     output = model.generate(
#         **inputs, 
#         max_length=50, 
#         do_sample=True,
#         temperature=0.7,
#         top_k=50,
#         top_p=0.9
#     )
#     inference_end = time.time()
    
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     print(f"🔍 Inferencia completada en {inference_end - inference_start:.2f} segundos.".encode("utf-8", "ignore").decode("utf-8"))
#     print("\n💬 Respuesta generada:".encode("utf-8", "ignore").decode("utf-8"))
#     print(response)

# except Exception as e:
#     print(f"❌ Error al ejecutar el modelo: {e}".encode("utf-8", "ignore").decode("utf-8"))

# finally:
#     print("🧩 Liberando memoria...".encode("utf-8", "ignore").decode("utf-8"))


#     # 📌 Eliminar variables solo si existen
#     if 'model' in locals():
#         del model
#     if 'tokenizer' in locals():
#         del tokenizer

#     # 📌 Liberar caché de GPU y recolectar basura
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
    
#     gc.collect()

#     print("✅ Memoria liberada.".encode("utf-8", "ignore").decode("utf-8"))

#     # 🔍 Verificar y eliminar procesos zombies y huérfanos
#     zombie_found = False
#     orphan_found = False
#     system_os = platform.system().lower()  # Detectar sistema operativo (windows/linux/macos)

#     for proc in psutil.process_iter(['pid', 'name', 'status', 'ppid']):
#         try:
#             pid = proc.info['pid']
#             ppid = proc.info['ppid']
#             status = proc.info['status']

#             # 🧟‍♂️ Si es un proceso zombie
#             if status == psutil.STATUS_ZOMBIE:
#                 print(f"⚠️ Proceso zombie detectado: PID {pid} (Padre: {ppid})".encode("utf-8", "ignore").decode("utf-8"))

#                 if ppid > 1:
#                     try:
#                         parent = psutil.Process(ppid)
#                         print(f"⚙️ Notificando al padre (PID {ppid}) para eliminar el zombie...".encode("utf-8", "ignore").decode("utf-8"))
#                         parent.wait()
#                     except psutil.NoSuchProcess:
#                         print(f"❌ Padre no existe. Intentando eliminación manual...".encode("utf-8", "ignore").decode("utf-8"))
#                         psutil.Process(pid).kill()  # 🚀 Eliminación segura
#                 else:
#                     print(f"❌ Zombie sin padre válido. Eliminando PID {pid}...".encode("utf-8", "ignore").decode("utf-8"))
#                     psutil.Process(pid).kill()

#             # 🏚️ Si es huérfano (PPID = 1 y no es zombie, pero sigue activo)
#             elif ppid == 1 and status not in [psutil.STATUS_ZOMBIE, psutil.STATUS_STOPPED]:
#                 print(f"⚠️ Proceso huérfano detectado: PID {pid}. Finalizando...".encode("utf-8", "ignore").decode("utf-8"))
#                 psutil.Process(pid).kill()  # 🚀 Eliminación segura

#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, PermissionError) as e:
#             print(f"⚠️ No se pudo eliminar el proceso PID {pid}: {e}".encode("utf-8", "ignore").decode("utf-8"))

# # ✅ Si no se encontraron procesos zombies
# if not zombie_found:
#     print(f"✅ No se encontraron procesos zombie 🧟".encode("utf-8", "ignore").decode("utf-8"))

# # ✅ Si no se encontraron procesos huérfanos
# if not orphan_found:
#     print(f"✅ No se encontraron procesos huérfanos 🏚️".encode("utf-8", "ignore").decode("utf-8"))

# total_time = time.time() - start_time
# print(f"⏱️ Tiempo total de ejecución: {total_time:.2f} segundos.".encode("utf-8", "ignore").decode("utf-8"))
