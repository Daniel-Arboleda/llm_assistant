import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 📌 Verificar disponibilidad de GPU
print("🚀 Verificando disponibilidad de GPU...")
gpu_available = torch.cuda.is_available()

# 📌 Configuración de memoria (ajustable)
GPU_MEMORY_LIMIT_GB = 3  # 🔧 Ajusta el límite de memoria de GPU
TOTAL_GPU_MEMORY_GB = torch.cuda.get_device_properties(0).total_memory / 1e9 if gpu_available else 0

if gpu_available:
    print(f"✅ GPU detectada: {torch.cuda.get_device_name(0)} con {TOTAL_GPU_MEMORY_GB:.2f} GB")

    # 📌 Establecer límite de memoria de GPU si es posible
    memory_fraction = min(GPU_MEMORY_LIMIT_GB / TOTAL_GPU_MEMORY_GB, 1)
    torch.cuda.set_per_process_memory_fraction(memory_fraction, 0)

    # 📌 Evitar fragmentación de memoria en CUDA
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

else:
    print("⚠️ No se detectó GPU. El modelo se ejecutará en CPU.")

# 📌 Ruta donde se guardará el modelo
model_path = "./model"

# 📌 Verificar si el modelo ya está descargado
if not os.path.exists(model_path) or not os.listdir(model_path):
    print("🔽 Descargando el modelo GPT-Neo 1.3B...")

    try:
        # 📌 Cargar modelo optimizando el uso mixto de GPU y RAM
        model = AutoModelForCausalLM.from_pretrained(
            "EleutherAI/gpt-neo-1.3B",
            torch_dtype=torch.float16 if gpu_available else torch.float32,  # Reducir consumo de memoria
            device_map="auto" if gpu_available else None,  # Asignación automática de GPU y RAM
            offload_folder="./offload" if gpu_available else None,  # Mover partes del modelo a RAM si es necesario
            low_cpu_mem_usage=True
        )
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

        # 📌 Guardar el modelo en la carpeta local
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
        print("✅ Modelo descargado y guardado en:", model_path)

    except ImportError:
        print("❌ Error: Falta un paquete requerido. Ejecuta:")
        print("    pip install accelerate")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

else:
    print("✅ El modelo ya está descargado. No se necesita descargar nuevamente.")
