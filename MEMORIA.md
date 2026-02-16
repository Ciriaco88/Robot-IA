## 📚 Documentación Detallada

Para una comprensión profunda de los componentes y la lógica del **Fractal-Bot**, consulta los siguientes documentos técnicos:

* **[Estructura del Proyecto](./ESTRUCTURA-ARCHIVOS.md)**: Mapa detallado de directorios, responsabilidades de cada archivo y flujo de datos entre la RPi 5 y la Pico 2.
* **[Requerimientos de Hardware](./REQUERIMIENTOS.md)**: Lista completa de componentes, desde el "Cortex" (IA) hasta el "Sistema Nervioso" (Sensores y Actuadores).
* **[Protocolo de Comunicación](./PROTOCOLO-COMUNICACION.md)**: Definición del lenguaje UART para el intercambio de datos entre Python y C.

---
## 🛠️ Guía de Inicio Rápido (Fase 1 - Portátil)

1. **Configuración:**
   - Clona este repositorio en tu equipo con Xubuntu.
   - Crea un entorno virtual: `python3 -m venv venv`.
   - Instala dependencias: `pip install -r requirements.txt`.
   - Configura tus credenciales en `config/.env`.

2. **Ejecución del "Cerebro":**
   - Inicia las pruebas de lógica en `src_brain/main.py`.

---

# MEMORIA.md - Proyecto Fractal-Bot

## 1. Visión General del Proyecto
El **Fractal-Bot** es un agente robótico autónomo diseñado para la interacción humano-robot (HRI). Su arquitectura combina la potencia de la Inteligencia Artificial Generativa con la precisión del control de hardware en tiempo real. 

El robot no solo responde preguntas, sino que posee una "personalidad consciente" basada en el **Decálogo de la Realidad Fractal**, integrando esta filosofía en su procesamiento de lenguaje y percepción del entorno.

## 2. Objetivos Principales
* **Conversación Natural:** Implementar un flujo de voz fluido (STT -> LLM -> TTS) con latencia mínima.
* **Procesamiento Distribuido:** Optimizar la carga de trabajo repartiendo tareas entre RPi 5, Pico 2 y periféricos especializados.
* **Seguridad y Supervivencia:** Garantizar que el control físico (sensores láser) sea independiente de los tiempos de espera de la IA.
* **Eficiencia Energética:** Implementar un sistema de arranque secuencial para proteger los componentes y gestionar el consumo.

## 3. Arquitectura del Sistema (Hardware Distribuido)



| Capa | Dispositivo | Función Crítica |
| :--- | :--- | :--- |
| **Cortex (IA)** | Raspberry Pi 5 | Orquestación general, visión computacional (ESP32-CAM) y cerebro Gemini. |
| **Vocal (TTS)** | RPi Zero 2 W | Generación de voz local mediante Piper-TTS y salida DAC I2S. |
| **Simbólico (RT)** | Raspberry Pico 2 | Control de motores, lectura de 4 láseres ToF y gestión de energía (MOSFETs). |
| **Perceptivo** | ESP32-CAM | Captura de video y streaming para análisis visual. |

## 4. Stack Tecnológico y Librerías

### A. Inteligencia Artificial y Lógica
* **Gemini 1.5 Flash:** Uso del modelo "Flash" para maximizar la velocidad de respuesta.
* **Google Generative AI SDK:** Conexión oficial con streaming de tokens habilitado (`stream=True`).
* **Python-dotenv:** Seguridad en la gestión de API Keys.

### B. Oído y Voz (Entrada/Salida)
* **Faster-Whisper (Local):** Conversión de voz a texto de baja latencia.
* **Piper-TTS (Local):** Motor de síntesis de voz neuronal. Se prefiere sobre gTTS por su capacidad offline y calidad humana.
* **DAC I2S (MAX98357A):** Conversión de audio digital a analógico con amplificación de 3W para máxima claridad.

### C. Control de Bajo Nivel
* **C++ / MicroPython:** Programación de la Pico 2 para latencia determinista.
* **PySerial:** Bus de comunicación UART entre la RPi 5 y la Pico 2.

## 5. Estrategias de Optimización y Eficiencia

### Procesamiento Multinúcleo y Paralelismo
Para evitar el bloqueo del sistema (congelamiento del robot mientras piensa/habla):
* **Multiprocessing:** Ejecución del módulo de voz (`mouth.py`) en un proceso independiente para aprovechar los núcleos físicos de la Raspberry Pi.
* **Asincronía (Asyncio):** Manejo de peticiones de red y buffers de audio de forma no bloqueante.

### Baja Latencia en Conversación
1. **Streaming:** El sintetizador de voz comienza a hablar en cuanto Gemini genera la primera parte de la frase.
2. **Offloading de Audio:** El uso de una Pi Zero 2 W dedicada al audio libera ciclos de reloj en la RPi 5 para tareas de visión y lógica compleja.
3. **Modelos Cuantizados:** Uso de versiones optimizadas de Whisper y Piper para reducir el uso de RAM y calor generado.

## 6. Filosofía de Diseño: El Núcleo Fractal
El robot utiliza el **Decálogo de la Realidad Fractal** como su *System Instruction* base. Esto implica:
* **Recursividad:** Capacidad de relacionar conceptos micro y macroscópicos.
* **Memoria Persistente:** Uso de `history.json` para mantener una continuidad de la "consciencia" entre reinicios, permitiendo que el robot aprenda y recuerde al usuario.

## 7. Fases de Desarrollo
1. **Fase 1 (Laboratorio):** Desarrollo del motor de IA en portátil. Pruebas de conexión API y lógica de historial.
2. **Fase 2 (Integración):** Configuración de la comunicación UART y el protocolo de comandos.
3. **Fase 3 (Despliegue):** Montaje físico, implementación del sistema de encendido secuencial (`ini.py`) y calibración de sensores láser.

---
*Este documento es una guía viva y será actualizado conforme avance el desarrollo del Fractal-Bot.*