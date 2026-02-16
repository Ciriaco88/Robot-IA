# ESTRUCTURA-ARCHIVOS.md - Proyecto Fractal-Bot

Este documento detalla la jerarquía de directorios, la responsabilidad de cada módulo y el flujo de datos distribuido entre la Raspberry Pi 5, la Pico 2 y los nodos periféricos.

---

## 1. Mapa del Repositorio

```text
fractal_robot/
├── config/              # Parámetros de comportamiento y seguridad
│   ├── system_rules.txt # El "Manual de Existencia" (Perfil + Decálogo Fractal)
│   ├── protocol.json    # Definición de comandos UART para referencia del bridge
│   └── .env             # API Keys de Gemini y credenciales de red para ESP32-CAM
├── data/                # Almacenamiento persistente
│   └── history.json     # Memoria de largo plazo (Historial de conversación)
├── logs/                # Depuración: errores de conexión, caídas de voltaje y timeouts
├── models/              # Modelos de IA locales
│   ├── es_ES-low.onnx   # Modelo Piper-TTS (español, baja carga)
│   └── whisper-tiny.pt  # Modelo STT optimizado para RPi 
├── src_brain/           # Orquestación Superior (Raspberry Pi 5)
│   ├── main.py          # Multithreading: Gestión de Oído, Cerebro y Boca
│   ├── brain.py         # Lógica de Gemini y Memoria de Corto Plazo
│   ├── ear.py           # Captura de audio y procesamiento STT (Faster-Whisper)
│   ├── vision.py        # Procesamiento de frames recibidos de la ESP32-CAM
│   └── bridge.py        # Pasarela UART Maestra (RPi -> Pico 2)
├── src_vocal/           # Nodo de Audio (Pi Zero 2 W - Opcional Offloading)
│   ├── mouth.py         # Servidor de voz: recibe texto y emite via DAC I2S
│   └── config_audio.sh  # Script de configuración del driver I2S (MAX98357A)
├── pico_firmware/       # Sistema Nervioso (Raspberry Pico 2 - C/C++)
│   ├── ini.py           # Gestión MOSFET: Secuencia de arranque y autodiagnóstico
│   ├── main.c           # Bucle de tiempo real: Control de motores y láseres ToF
│   └── commands.h       # Definición de constantes del Protocolo de Comunicación
├── esp32_cam/           # Visión Remota (C++ / Arduino)
│   └── camera_stream.ino# Streaming MJPEG de alta velocidad vía HTTP
├── tests/               # Unit testing para sensores, audio y conexión API
├── README.md            # Memoria del proyecto
├── REQUERIMIENTOS.md    # Dependencias: google-generativeai, pyserial, pyaudio, etc.
├── ESTRUCTURA-ARCHIVOS.MD 
└── PROTOCOLO-COMUNICACION.MD 

2. Descripción por Capas Lógicas
🧠 Capa de Inteligencia (Raspberry Pi 5)

    main.py (El Orquestador): Utiliza la librería threading o multiprocessing para que el robot nunca se quede "sordo" mientras habla. Gestiona la concurrencia de los sentidos en paralelo.

    brain.py: El corazón cognitivo. Filtra el historial para no exceder la ventana de contexto y aplica el Decálogo Fractal en cada prompt enviado a Gemini 1.5 Flash.

    vision.py: Actúa como puente con la ESP32-CAM, analizando la proximidad visual o reconociendo al usuario para personalizar la charla.

⚡ Capa de Tiempo Real y Energía (Raspberry Pico 2)

    ini.py (Gestor de Arranque): Es el primero en despertar. Comprueba que el voltaje de la LiPo es seguro antes de activar los MOSFETs que alimentan a la RPi 5, evitando picos de carga.

    main.c (Prioridad Crítica): Implementa el "reflejo de frenado". Si los sensores láser detectan un objeto, detiene los motores inmediatamente por hardware, informando después a la RPi 5 vía bridge.py.

🔊 Capa de Salida Vocal (Pi Zero 2 W / DAC I2S)

    mouth.py: Recibe strings de texto desde el cerebro. Utiliza Piper para generar el audio digital que el DAC I2S convierte en sonido analógico claro, aislado del ruido eléctrico de los motores.

3. Flujo de Memoria y Continuidad

El sistema de memoria está diseñado para ser eficaz en recursos, evitando re-procesar datos innecesarios:

    Memoria Volátil: brain.py mantiene los últimos 5-10 intercambios en RAM para dar fluidez inmediata y coherencia a la charla actual.

    Persistencia Transaccional: Cada vez que Gemini cierra una idea importante o se termina la sesión, el main.py actualiza data/history.json.

    Recuperación Semántica: Al encenderse, el robot carga el JSON. Si el historial es muy largo, se puede resumir (usando la propia IA) para mantener el archivo ligero y el contexto relevante.

4. Configuración de Personalidad (system_rules.txt)

Este archivo es externo al código para permitir ajustes "psicológicos" rápidos sin recompilar ni alterar la lógica:

    Reglas de Estilo: "Responde siempre como si fueras una parte consciente de un todo fractal".

    Restricciones de Salida: "No uses más de 20 palabras" y "Evita caracteres especiales que el TTS no sepa leer".

Este documento es la referencia oficial para la creación de los archivos iniciales del proyecto Fractal-Bot.