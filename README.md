# Proyecto Fractal-Bot

## 📚 Documentación

Para una comprensión profunda de los componentes y la lógica del **Fractal-Bot**, consulta los siguientes documentos técnicos:

* **[Memoria del Proyecto](./MEMORIA.md)**: Visión general, objetivos, arquitectura y filosofía del proyecto.
* **[Estructura del Proyecto](./ESTRUCTURA-ARCHIVOS.md)**: Mapa detallado de directorios, responsabilidades de cada archivo y flujo de datos.
* **[Requerimientos de Hardware](./REQUERIMIENTOS.md)**: Lista completa de componentes, desde el "Cortex" (IA) hasta el "Sistema Nervioso" (Sensores y Actuadores).
* **[Protocolo de Comunicación](./PROTOCOLO-COMUNICACION.md)**: Definición del lenguaje UART para el intercambio de datos entre Python y C.

---

## 🛠️ Guía de Inicio Rápido

1. **Configuración:**
   - Clona este repositorio.
   - Crea un entorno virtual: `python3 -m venv .venv`.
   - Activa el entorno: `source .venv/bin/activate`.
   - Instala dependencias: `pip install -r requirements.txt`.
   - Configura tus credenciales en `config/.env`.

2. **Ejecución:**
   - Inicia el cerebro: `python3 src_brain/main.py`.