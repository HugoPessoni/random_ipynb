import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados
df = pd.read_csv('vibracoes.csv')

# Plota os dados do acelerômetro
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(df['AccelX'], label='Accel X')
plt.plot(df['AccelY'], label='Accel Y')
plt.plot(df['AccelZ'], label='Accel Z')
plt.title('Acelerômetro')
plt.xlabel('Amostra')
plt.ylabel('g')
plt.legend()

'''# Plota os dados do giroscópio
plt.subplot(2, 1, 2)
plt.plot(df['GyroX'], label='Gyro X')
plt.plot(df['GyroY'], label='Gyro Y')
plt.plot(df['GyroZ'], label='Gyro Z')
plt.title('Giroscópio')
plt.xlabel('Amostra')
plt.ylabel('°/s')
plt.legend()'''

plt.tight_layout()
plt.show()
