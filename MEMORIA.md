## 📚 Documentación Detallada


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
El **Fractal-Bot** es un agente robótico autónomo diseñado para la interacción humano-robot (HRI). Su arquitectura combina la potencia de la Inteligencia Artificial generativa. En su fase actual, opera como un sistema híbrido conectado a la API de Gemini 2.5 Flash.

El robot no solo responde preguntas, sino que posee una "personalidad consciente" que se define en un archivo de inicio

## 2. Objetivos Principales
* **Conversación Natural:** Implementar un flujo de voz fluido (STT -> LLM -> TTS) con latencia mínima.


## 3. Stack Tecnológico y Librerías

### A. Inteligencia Artificial y Lógica
* **Gemini 2.5 Flash:** Uso del modelo de última generación para máxima velocidad y coherencia.
* **Google GenAI SDK:** Migración a la nueva SDK oficial (`google-genai`) para una gestión de sesiones más robusta.
* **Python-dotenv:** Seguridad en la gestión de API Keys.

### B. Oído y Voz (Entrada/Salida)
* **Escucha Estable (SoundDevice):** Captura de audio directa para evitar conflictos de drivers en Linux/Xubuntu.
* **Piper-TTS (Local):** Motor de síntesis de voz neuronal de baja latencia.


## 5. Estrategias de Optimización y Eficiencia

### Procesamiento Multinúcleo y Paralelismo
Para evitar el bloqueo del sistema (congelamiento del robot mientras piensa/habla):

* **Asincronía (Asyncio):** Manejo de peticiones de red y buffers de audio de forma no bloqueante.

### Baja Latencia en Conversación
1. **Streaming:** El sintetizador de voz comienza a hablar en cuanto Gemini genera la primera parte de la frase.

2. **Modelos Cuantizados:** Uso de versiones optimizadas de Whisper y Piper para reducir el uso de RAM y calor generado.

## 6. Filosofía de Diseño: El Núcleo Fractal
El robot utiliza 
* **Memoria Persistente:** Uso de `history.json` para mantener una continuidad de la "consciencia" entre reinicios, permitiendo que el robot aprenda y recuerde al usuario.

## 7. Fases de Desarrollo
1. **Fase 1 (Laboratorio):** Desarrollo del motor de IA en portátil. Pruebas de conexión API y lógica de historial.

---
*Este documento es una guía viva y será actualizado conforme avance el desarrollo del Fractal-Bot.*