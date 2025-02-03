import time
import smbus
import amg8833_i2c

try:
    #
    # Inicializa a câmera térmica
    #
    sensor_ligado = True
    t0 = time.time()
    sensor = []
    while (time.time()-t0)<1: # wait 1sec for sensor to start
        try:
            # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
            sensor = amg8833_i2c.AMG8833(addr=0x69, bus_num=3) # start AMG8833
        except:
            sensor = amg8833_i2c.AMG8833(addr=0x68, bus_num=3)
        finally:
            pass
    time.sleep(0.1) # wait for sensor to settle

    # Se o módulo não foi encontrado
    if sensor==[]:
        sensor_ligado = False

    
    if sensor_ligado == True:
        contador = 0
        coleta = 0
        sum_amb = 0
        sum_alvo = 0
        media_amb = 0
        media_alvo = 0
        while contador < 10:
            #
            # Leitura da câmera térmica
            #
            pix_to_read = 64 # read all 64 pixels
            h_temp = []
            arr_temp = []

            status,pixels = sensor.read_temp(pix_to_read) # read pixels with status
            if status: # if error in pixel, re-enter loop and try again
                continue

            for x in range(pix_to_read):
                if pixels[x] <= 26:
                    pixels[x] = 20

            arr_temp = pixels.copy()
            arr_temp.sort(reverse=True)
            arr_temp[0] += 5.5
            arr_temp[1] += 5.5
            arr_temp[2] += 5.5
            
            T_thermistor = sensor.read_thermistor() # lê o thermistor
            T_thermistor = float(T_thermistor) - 1.5
            print("Temperatura Ambiene: {0:2.2f}".format(T_thermistor))
            print("Temperatura Alvo:",arr_temp[0])
            print("------------------")
            presenca = 0
            if arr_temp[0] > 32:
                presenca = 1

            sum_amb = sum_amb + T_thermistor
            sum_alvo = sum_alvo + arr_temp[0]

            coleta = coleta + 1

            contador = contador + 1

            time.sleep(.1)

        media_amb = sum_amb/coleta
        media_alvo = sum_alvo/coleta
        self.temp_ambiente_ponto = "{:2.2f}".format(media_amb)
        self.temp_alvo_ponto = media_alvo

    # bus = SMBus(3)

    # sensor = MLX90614(bus, address=0x5A)

    # self.temp_ambiente_ponto = "{:.2f}".format(sensor.get_amb_temp())
    # self.temp_alvo_ponto =  "{:.2f}".format(sensor.get_obj_temp())

    # bus.close()
except:                    
    # try:
    #     i2c = io.I2C(board.SCL, board.SDA, frequency=100000)

    #     mlx = adafruit_mlx90614.MLX90614(i2c)
    #     self.temp_ambiente_ponto = "{:.2f}".format(mlx.ambient_temperature)
    #     self.temp_alvo_ponto = "{:.2f}".format(mlx.object_temperature)
    # except:
    #     time.sleep(1)
    #     self.get_temp()
    pass
