import gps
import time
import math
import pandas as pd
from datetime import datetime
import serial
import multiprocessing
import random
import string
import cv2
import wiringpi
from wiringpi import GPIO
import signal
import sys

# Definição dos pinos
LED_VERDE = 2     # LED verde
LED_VERMELHO = 3  # LED vermelho
LED_AMARELO = 4   # LED amarelo
LED_AZUL = 5      # LED azul
BUTTON1_PIN = 0   # Botão 1 (início da gravação)
BUTTON2_PIN = 1   # Botão 2 (encerramento da gravação)

# Configuração inicial do GPIO
wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_VERDE, GPIO.OUTPUT)
wiringpi.pinMode(LED_VERMELHO, GPIO.OUTPUT)
wiringpi.pinMode(LED_AMARELO, GPIO.OUTPUT)
wiringpi.pinMode(LED_AZUL, GPIO.OUTPUT)
wiringpi.pinMode(BUTTON1_PIN, GPIO.INPUT)
wiringpi.pinMode(BUTTON2_PIN, GPIO.INPUT)
wiringpi.pullUpDnControl(BUTTON1_PIN, wiringpi.PUD_UP)
wiringpi.pullUpDnControl(BUTTON2_PIN, wiringpi.PUD_UP)

def get_id(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    id_unico = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return id_unico

def save_results_to_xlsx(data_list, id, tipo):
    filename = f"/home/orangepi/{tipo}_{id}.xlsx"
    headers = ['time', 'lat', 'lon', 'speed']
    df = pd.DataFrame(data_list, columns=headers)
    df.to_excel(filename, index=False)
    print(f"Dados salvos em {filename}")
    return True  # Para indicar que o salvamento foi bem-sucedido

def gps_antigo(id, stop_event, erro_event):
    print('antigo')

    def gps_time_to_datetime(gps_date, gps_time):
        try:
            date_time_str = gps_date + gps_time
            return datetime.strptime(date_time_str, "%d%m%y%H%M%S")
        except ValueError as e:
            print(f"Erro ao converter data e hora do GPS: {e}")
            return None

    try:
        ser = serial.Serial('/dev/ttyS7', baudrate=9600, timeout=0.1)
    except Exception as e:
        print(f"Erro ao conectar ao GPS na porta serial: {e}")
        erro_event.set()
        return

    print("Conexão com GPS estabelecida.")
    data_list = []
    while not stop_event.is_set():
        try:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line.startswith('$GNRMC'):
                parts = line.split(',')
                if parts[2] == 'A':
                    lat = float(parts[3][:2]) + float(parts[3][2:]) / 60.0
                    lon = float(parts[5][:3]) + float(parts[5][3:]) / 60.0
                    if parts[4] == 'S':
                        lat = -lat
                    if parts[6] == 'W':
                        lon = -lon
                    speed = float(parts[7]) * 0.514444
                    current_time = gps_time_to_datetime(parts[9], parts[1][:6])
                    data_list.append([current_time, lat, lon, f"{speed:.3f}"])
                    
                    print("--------------------------------------")
                    print("Dados TPV Recebidos gps antigo:")
                    print(f"  time: {current_time}")
                    print(f"  lat: {lat}")
                    print(f"  lon: {lon}")
                    print(f"  speed: {speed:.3f} m/s")
                    print("--------------------------------------")
                                        
        except Exception as e:
            print(f"Erro ao processar os dados do GPS antigo: {e}")
            erro_event.set()

    if data_list:
        save_results_to_xlsx(data_list, id, "GPS_Antigo")

def gps_novo(id, stop_event, erro_event):
    print('novo')

    def nmea_time_to_datetime(nmea_time, nmea_date):
        time_str = nmea_date + nmea_time[:6]
        return datetime.strptime(time_str, "%d%m%y%H%M%S")

    def process_nmea_sentence(sentence):
        parts = sentence.split(',')
        if sentence.startswith('$GNRMC'):
            return {
                'type': 'RMC',
                'time': parts[1],
                'status': parts[2],
                'lat': float(parts[3][:2]) + float(parts[3][2:]) / 60.0 * (-1 if parts[4] == 'S' else 1),
                'lon': float(parts[5][:3]) + float(parts[5][3:]) / 60.0 * (-1 if parts[6] == 'W' else 1),
                'speed': float(parts[7]) * 0.51444,
                'date': parts[9]
            }
        return None

    try:
        ser = serial.Serial('/dev/ttyS3', baudrate=38400, timeout=0.1)
        print("Conectado ao GPS")
    except Exception as e:
        print(f"Erro ao conectar ao GPS: {e}")
        erro_event.set()
        return

    data_list = []
    while not stop_event.is_set():
        try:
            data = ser.readline().decode('ascii', errors='replace').strip()
            if data:
                nmea_data = process_nmea_sentence(data)
                if nmea_data and nmea_data['type'] == 'RMC' and nmea_data['status'] == 'A':
                    lat = nmea_data['lat']
                    lon = nmea_data['lon']
                    speed = nmea_data['speed']
                    current_time = nmea_time_to_datetime(nmea_data['time'], nmea_data['date'])
                    data_list.append([current_time, lat, lon, f"{speed:.3f}"])
                    
                    print("--------------------------------------")
                    print("Dados TPV Recebidos gps novo:")
                    print(f"  time: {current_time}")
                    print(f"  lat: {lat}")
                    print(f"  lon: {lon}")
                    print(f"  speed: {speed:.3f} m/s")
                    print("--------------------------------------")
                                        
        except Exception as e:
            print(f"Erro ao processar os dados do GPS novo: {e}")
            erro_event.set()

    if data_list:
        save_results_to_xlsx(data_list, id, "GPS_Novo")

def cam(id, stop_event, erro_event):
    print('camera')

    fps = 1  # Definir a taxa de quadros para 1 FPS
    frame_width, frame_height = 1920, 1080  # Definir a resolução para Full HD
    video_path = f'/home/orangepi/Video_{id}.mp4'
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        erro_event.set()
        return

    print("Iniciando gravação automaticamente")

    try:
        video_writer = cv2.VideoWriter(
            video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height)
        )

        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret and video_writer:
                video_writer.write(frame)
            time.sleep(1)  # Atraso de 1 segundo para corresponder ao FPS definido
    finally:
        if video_writer is not None:
            video_writer.release()
        cap.release()
        print(f"Vídeo salvo em {video_path}")
    return True

def main():
    id = get_id()
    stop_event = multiprocessing.Event()
    erro_event = multiprocessing.Event()

    # Conferir conexão com GPS e câmera
    p_cam_test = multiprocessing.Process(target=cam, args=(id, stop_event, erro_event))
    p_gps_novo_test = multiprocessing.Process(target=gps_novo, args=(id, stop_event, erro_event))
    p_gps_antigo_test = multiprocessing.Process(target=gps_antigo, args=(id, stop_event, erro_event))

    p_cam_test.start()
    p_gps_novo_test.start()
    p_gps_antigo_test.start()

    p_cam_test.join(3)
    p_gps_novo_test.join(3)
    p_gps_antigo_test.join(3)

    if erro_event.is_set():
        wiringpi.digitalWrite(LED_VERMELHO, GPIO.HIGH)
        while True:
            wiringpi.digitalWrite(LED_VERMELHO, GPIO.HIGH)
            time.sleep(0.5)
            wiringpi.digitalWrite(LED_VERMELHO, GPIO.LOW)
            time.sleep(0.5)
    else:
        wiringpi.digitalWrite(LED_VERDE, GPIO.HIGH)

    # Espera pelo início da gravação
    while wiringpi.digitalRead(BUTTON1_PIN) == GPIO.HIGH:
        time.sleep(0.1)

    # Inicia a gravação
    wiringpi.digitalWrite(LED_AMARELO, GPIO.HIGH)
    p_cam = multiprocessing.Process(target=cam, args=(id, stop_event, erro_event))
    p_gps_novo = multiprocessing.Process(target=gps_novo, args=(id, stop_event, erro_event))
    p_gps_antigo = multiprocessing.Process(target=gps_antigo, args=(id, stop_event, erro_event))

    p_cam.start()
    p_gps_novo.start()
    p_gps_antigo.start()

    # Monitoramento constante do botão 2
    try:
        while True:
            if wiringpi.digitalRead(BUTTON2_PIN) == GPIO.LOW:  # Botão 2 foi pressionado
                stop_event.set()
                break
            time.sleep(0.1)
    finally:
        p_cam.join()
        p_gps_novo.join()
        p_gps_antigo.join()

        wiringpi.digitalWrite(LED_AMARELO, GPIO.LOW)
        wiringpi.digitalWrite(LED_VERDE, GPIO.LOW)

        # Verifica se o salvamento foi bem-sucedido
        if erro_event.is_set():
            wiringpi.digitalWrite(LED_VERMELHO, GPIO.HIGH)
            time.sleep(3)
            wiringpi.digitalWrite(LED_VERMELHO, GPIO.LOW)
        else:
            wiringpi.digitalWrite(LED_AZUL, GPIO.HIGH)
            time.sleep(3)
            wiringpi.digitalWrite(LED_AZUL, GPIO.LOW)

if __name__ == "__main__":
    main()
