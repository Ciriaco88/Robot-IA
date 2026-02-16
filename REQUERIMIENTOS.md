# REQUERIMIENTOS.md - Proyecto Fractal-Bot

Este documento detalla el hardware, software y las especificaciones técnicas necesarias para la construcción del robot cognitivo basado en Gemini, RPi 5 y Pico 2.

## 1. Hardware Principal (Computación Distribuida)

| Componente | Función | Notas Técnicas |
| :--- | :--- | :--- |
| **Raspberry Pi 5** | Cerebro Superior | Orquestación de IA, Visión y lógica de Gemini. |
| **Raspberry Pico 2** | Cerebro Reptiliano | Control en tiempo real, seguridad, láseres y motores. |
| **ESP32-CAM** | Ojo Periférico | Streaming de video MJPEG vía WiFi/HTTP. |
| **RPi Zero 2 W** | Módulo de Voz | (Opcional) Dedicada exclusivamente a Piper-TTS. |

## 2. Audio y Sonido (Opciones de Desarrollo)

Para optimizar la **eficacia de recursos**, se prioriza la descarga de procesos de audio:

* **Opción I2S (Recomendada por Eficiencia):**
    * **Hardware:** DAC I2S (ej. MAX98357A o UDA1334A).
    * **Conexión:** Pines GPIO dedicados (Bit Clock, Word Select, Data).
    * **Ventaja:** Salida digital pura, mínima carga de CPU, sin interferencias de motores.
* **Opción USB (Prototipado):**
    * **Hardware:** Tarjeta de sonido USB genérica.
    * **Ventaja:** Implementación inmediata ("Plug & Play").

## 3. Sensores y Actuadores (Sistema Nervioso)

* **Movilidad:** 2 Motores DC con reductora para tracción diferencial.
* **Control de Potencia:** Puente H TB6612FNG (más eficiente térmicamente que el L298N).
* **Percepción Espacial:** 4 Sensores Láser ToF (VL53L0X) vía I2C a la Pico 2.
* **Gestión de Energía:** MOSFETs de potencia para el encendido secuencial de periféricos controlado por la Pico 2 (`ini.py`).

## 4. Software y Stack Tecnológico

### Inteligencia Artificial
- **Modelo:** Gemini 1.5 Flash (vía `google-generativeai`).
- **Contexto:** Instrucciones de sistema basadas en el **Decálogo de la Realidad Fractal**.

### Voz y Oído
- **STT (Voz a Texto):** `SpeechRecognition` con Whisper (modelo base/tiny).
- **TTS (Texto a Voz):** `Piper-TTS` con modelos ONNX locales en español (ej. `es_ES-low`).

### Comunicación y Protocolos
- **Capa Física:** UART (Serie) a 115,200 bps.
- **Protocolo de Datos:** Formato de trama de texto `[ORIGEN]>[DESTINO]:[COMANDO]:[VALORES]`.
- **Librerías Python:** `pyserial`, `python-dotenv`, `pyaudio`, `asyncio`.

## 5. Especificaciones de Energía
- **Batería:** LiPo de 7.4V (2S) o 11.1V (3S) recomendada.
- **Regulación:** Conversores Step-Down (Buck) independientes para 5V (RPi 5) y 3.3V (Sensores).
- **Seguridad:** Monitorización de voltaje mediante el ADC de la Raspberry Pico 2.

---
*Última actualización: Febrero 2026*