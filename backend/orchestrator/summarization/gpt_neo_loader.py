import torch
import gc
import os
import signal
import psutil
import logging
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "C:/Users/danie/OneDrive/Documentos/llm_assistant/backend/orchestrator/summarization/model/model")

# Configuración de logging profesional con carpeta centralizada
LOG_DIR = "C:/Users/danie/OneDrive/Documentos/llm_assistant/backend/orchestrator/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Asegurar que la carpeta de logs existe
LOG_FILE = os.path.join(LOG_DIR, "gpt_neo_loader.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Guardar logs en archivo
        logging.StreamHandler()  # Mostrar logs en consola
    ]
)

def clear_memory():
    """
    🧹 Limpia la memoria GPU y CPU para evitar fugas.
    """
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        logging.info("🔄 Memoria limpiada correctamente.")
    except Exception as e:
        logging.error(f"⚠️ Error al limpiar memoria: {e}")

def terminate_zombie_processes():
    """
    🚫 Termina procesos zombies o huérfanos que puedan estar ocupando memoria.
    """
    current_pid = os.getpid()
    try:
        for proc in psutil.process_iter(attrs=['pid', 'ppid', 'name']):
            if proc.info['ppid'] == current_pid and proc.info['pid'] != current_pid:
                os.kill(proc.info['pid'], signal.SIGTERM)
                logging.info(f"✅ Proceso zombie {proc.info['pid']} ({proc.info['name']}) terminado correctamente.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        logging.warning(f"⚠️ No se pudo eliminar un proceso zombie: {e}")

def load_model(model_name="EleutherAI/gpt-neo-125M", use_gpu=True):
    """
    🚀 Carga el modelo GPT-Neo-125M desde almacenamiento local o lo descarga si es necesario.
    """
    device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
    logging.info(f"🔄 Cargando modelo GPT-Neo-125M en {device}...")
    
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)

        # Si el modelo ya está en la ruta local, cargarlo desde allí
        if os.path.exists(MODEL_PATH):
            logging.info(f"📂 Cargando modelo desde almacenamiento local: {MODEL_PATH}")
            model = GPTNeoForCausalLM.from_pretrained(MODEL_PATH).to(device)
        else:
            logging.info(f"🌐 Modelo no encontrado en {MODEL_PATH}, descargando desde Hugging Face...")
            model = GPTNeoForCausalLM.from_pretrained(model_name).to(device)
            model.save_pretrained(MODEL_PATH)  # Guardar para evitar futuras descargas
            tokenizer.save_pretrained(MODEL_PATH)

        logging.info("✅ Modelo GPT-Neo-125M cargado exitosamente.")
        return model, tokenizer
    except Exception as e:
        logging.error(f"❌ Error al cargar el modelo GPT-Neo-125M: {e}")
        return None, None

def release_model(model):
    """
    🔄 Libera memoria del modelo al finalizar.
    """
    try:
        if model:
            del model
            clear_memory()
            logging.info("🚀 Modelo GPT-Neo-125M liberado de memoria correctamente.")
    except Exception as e:
        logging.error(f"⚠️ Error al liberar el modelo GPT-Neo-125M: {e}")

if __name__ == "__main__":
    clear_memory()
    terminate_zombie_processes()
    
    model, tokenizer = load_model()

    logging.info("🤖 GPT-Neo-125M listo para generar texto.")
   
    inputs = {"input_ids": tokenizer.encode("Resumir reunión", return_tensors="pt")}
    output = model.generate(**inputs, max_length=300)
    summary = tokenizer.decode(output[0])

   
    
    logging.info(f"📝 Resumen estructurado generado:\n{structured_summary}")
    
    # Liberar memoria al finalizar
    release_model(model)
