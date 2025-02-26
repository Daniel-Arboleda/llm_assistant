# 🎬 Proyecto de Orquestación de IA para YouTube  

Este sistema permite extraer transcripciones de videos de YouTube, resumir su contenido utilizando IA y generar reportes.  

## 🏗️ Arquitectura del Proyecto  

📂 `orchestrator/`  
│── 📁 `api/` - 📡 Gestión de endpoints principales  
│── 📁 `transcriber/` - 🎙️ Extrae transcripciones de videos  
│── 📁 `youtube_downloader/` - ⬇️ Descarga audio de YouTube  
│── 📁 `whisper_transcriber/` - 📝 Conversión de audio a texto con Whisper  
│── 📁 `summarization_ai/` - 🤖 Resumen y procesamiento con LLM  
│── 📁 `report_generator/` - 📄 Generación de reportes en PDF  
│── 📁 `rag_database/` - 🧠 Base de datos vectorial para consultas  
│── 📝 `manage.py` - 🔧 Comando principal de Django  
│── 📦 `requirements.txt` - 📜 Dependencias del proyecto  

---

## 🚀 **Cómo Usar**  

### **1️⃣ Transcribir un Video**  
Enviar una petición `POST` a:  


# Arrancar script de monitoreo de recursos en tiempo real en segundo plano y con logs
python "C:\Users\danie\OneDrive\Documentos\llm_assistant\backend\orchestrator\logs\monitor.py"


# 🎯 Resultado esperado en la terminal

🔹 Monitoreo de RAM y CPU 🔹
   Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id ProcessName
   -------  ------    -----      ----- -----   ------     -- -----------
   1000     2000      1234567    2345678 5000  12.34      1234 chrome
   ...

🔹 Monitoreo de GPU 🔹
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 528.24                 Driver Version: 528.24                   |
|-------------------------------+----------------------+----------------------|
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf  Pwr:Usage/Cap| Memory-Usage | GPU-Util  Compute M. |
+-------------------------------+----------------------+----------------------|
|  0  RTX 3090     On    Off   | 00000000:01:00.0 Off |        0%     0%  |
|       55C    P8    15W / 350W |    1024MiB / 24576MiB |    0%      Default  |
+-------------------------------+----------------------+----------------------+

==================================================


