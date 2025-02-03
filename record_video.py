import cv2
import wiringpi
import signal
import time
from datetime import datetime

from wiringpi import GPIO

# Definição dos pinos
LED_PIN = 2  # Substitua pelo número do pino GPIO para o LED
BUTTON_PIN = 0  # Substitua pelo número do pino GPIO para o botão

# Configuração inicial
wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, GPIO.OUTPUT)
wiringpi.pinMode(BUTTON_PIN, GPIO.INPUT)
wiringpi.pullUpDnControl(BUTTON_PIN, wiringpi.PUD_UP)  # Habilita pull-up

# Variáveis de controle
led_on = False
recording = False
video_writer = None
fps = 30  # Defina o FPS para uma taxa de quadros mais baixa

# Manipulador para encerrar o programa
def signal_handler(sig, frame):
    wiringpi.digitalWrite(LED_PIN, GPIO.LOW)
    if video_writer:
        video_writer.release()
    print("programa encerrado")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Função para iniciar a gravação
def start_recording():
    global video_writer
    timestamp = datetime.now().strftime('%Y-%m-%d____%H-%M-%S-%f')
    video_path = f'/home/orangepi/video_{timestamp}.mp4'
    video_writer = cv2.VideoWriter(
        video_path, cv2.VideoWriter_fourcc(*'MJPG'), fps, (640, 480)
    )
    print(f"Iniciando gravação")
    return video_writer

# Função para parar a gravação
def stop_recording():
    global video_writer
    if video_writer:
        video_writer.release()
        video_writer = None
        print("Gravação parada")

# Configurar câmera
cap = cv2.VideoCapture(0)

print("Pressione Ctrl+C para sair")

while True:
    if wiringpi.digitalRead(BUTTON_PIN) == GPIO.LOW:
        led_on = not led_on  # Alterna o estado do LED
        recording = not recording

        wiringpi.digitalWrite(LED_PIN, GPIO.HIGH if led_on else GPIO.LOW)
        #print("leds on" if led_on else "leds off")

        if recording:
            video_writer = start_recording()
        else:
            stop_recording()

        time.sleep(0.5)  # Pequena pausa para evitar bouncing

    if recording:
        ret, frame = cap.read()
        if ret and video_writer:
            video_writer.write(frame)

    time.sleep(0.1)

cap.release()
