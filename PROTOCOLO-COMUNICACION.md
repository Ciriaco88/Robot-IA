Este documento establece el estándar de comunicación entre la Raspberry Pi 5 (Cerebro), la Pico 2 (Controlador de Motores/Sensores) y la ESP32-CAM (Ojo).

1. Configuración de la Capa Física

    Interfaz: UART (Universal Asynchronous Receiver-Transmitter).

    Baudrate: 115,200 bps.

    Paridad/Stop: 8N1 (8 bits, sin paridad, 1 bit de parada).

    Niveles Lógicos: 3.3V (¡Cuidado! No conectar 5V directamente a los GPIO de la RPi 5 o la Pico).

2. Formato de Trama (Frame Format)

Para facilitar el parseo en C (Pico 2) y Python (RPi 5), utilizaremos un formato basado en texto con terminador de línea:
[ORIGEN]>[DESTINO]:[COMANDO]:[VALORES]\n

3. Diccionario de Comandos (Mensajería)
A. De RPi 5 (Cerebro) a Pico 2 (Movimiento y Estado)

Comando	Parámetros	Descripción
MOT:VEL	v_izq,v_der	Ajusta velocidad de motores (-255 a 255).
MOT:STP	0	Parada suave e inmediata.
MOT:EMG	0	Parada de emergencia (corte de energía).
LED:MOD	id_color	Cambia el color del LED de estado (ej: 1=Pensando, 2=Escuchando).
B. De Pico 2 a RPi 5 (Telemetría y Alertas)
Comando	Parámetros	Descripción
SEN:LAS	d1,d2,d3,d4	Distancia en mm de los 4 sensores láser ToF.
STA:BAT	voltaje	Nivel de batería actual.
EVT:BUMP	id_sensor	Evento de colisión inminente (prioridad alta).
C. De ESP32-CAM a RPi 5 (Visión)

    Protocolo: Stream de video MJPEG vía HTTP (Puerto 80).

    Control: La RPi 5 enviará peticiones GET para cambiar resolución o activar el flash si Gemini detecta oscuridad.

4. Gestión de Errores y Prioridades

    Prioridad Crítica: Los mensajes EVT:BUMP o MOT:EMG tienen prioridad sobre cualquier procesamiento de Gemini.

    Timeouts: Si la RPi 5 no recibe el mensaje STA:BAT cada 10 segundos, entrará en modo de "Seguridad" y detendrá los motores.

    Checksum: (Opcional para Fase 2) Se añadirá un byte de suma al final si el ruido de los motores afecta a los datos.
