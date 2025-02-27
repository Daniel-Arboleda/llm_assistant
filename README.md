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

## 📁 Arquitectura por Capas
---------------------------------------------------------------------------------------------------------

---------------------|-----------------------|-----------------------|-----------------------
Capa 1: Presentación |                       |                       |                       |
---------------------|-----------------------|-----------------------|-----------------------
                     | Cliente Web/App       | Postman/API REST      | Otros Clientes       |
                     | - Envía solicitudes   | - Test API REST       | - Otros sistemas     |
                     | - Descarga resultados | - Automatización      | - Integraciones      |
---------------------|-----------------------|-----------------------|-----------------------

---------------------|-----------------------|-----------------------|-----------------------
Capa 2: Orquestación|       Orchestrator     |                       |                       |
---------------------|-----------------------|-----------------------|-----------------------
                     | - Recibe solicitudes  | - Redirige tráfico    | - Coordina servicios  |
                     | - Expone APIs REST    | - Maneja respuestas   | - Controla flujo      |
---------------------|-----------------------|-----------------------|-----------------------

---------------------|-----------------------|-----------------------|-----------------------
Capa 3: Microservicios |    Downloader      |   Transcriber         |   Summarization      |
---------------------|-----------------------|-----------------------|-----------------------
                        | - Descarga archivos | - Convierte audio    | - Genera resumen    |
                        | - Verifica formato  | - Usa Whisper        | - Usa GPT-Neo       |
                        | - Organiza archivos | - Guarda transcrip.  | - Filtra información|
---------------------|-----------------------|-----------------------|-----------------------
                        |          Report - Genera reportes en formato APA                |
---------------------|----------------------------------------------------------------------|
                        | Nota: Se propone integración futura del sistema con una APP      |
---------------------|----------------------------------------------------------------------|

---------------------|-----------------------|-----------------------|-----------------------
Capa 4: Almacenamiento |   Base de Datos     |   Archivos de Audio   |   Resúmenes Word     |
---------------------|-----------------------|-----------------------|-----------------------
                        | - SQLite/PostgreSQL| - Transcripciones     | - Documentos en .docx |
                        | - Bases de Datos   | - Archivos descargados | - Historial de reuniones |
                        |   Vectoriales      | - Almacenamiento local| - Metadatos de resúmenes |
---------------------|-----------------------|-----------------------|-----------------------



## 🚀 **Cómo Usar**  

### **1️⃣ Transcribir un Video**  
Enviar una petición `POST` a:  


# Arrancar script de monitoreo de recursos en tiempo real en segundo plano y con logs



# 🎯 Resultado esperado en la terminal

