import pandas as pd
import re

# Load csv
csv_path = '/mnt/data/dqn_metrics.csv'
csv_data = pd.read_csv(csv_path)

# load txt
txt_path = '/mnt/data/resultado_dqn.txt'
with open(txt_path, 'r') as file:
    txt_data = file.readlines()

# tirar metricas do txt
loss_updates = []
pattern = re.compile(r'total_timesteps\s*\|\s*(\d+).*?loss\s*\|\s*([\d\.]+).*?n_updates\s*\|\s*(\d+)', re.DOTALL)

for i, line in enumerate(txt_data):
    match = pattern.search(" ".join(txt_data[i:i+20]))
    if match:
        total_timesteps = int(match.group(1))
        loss = float(match.group(2))
        n_updates = int(match.group(3))
        loss_updates.append((total_timesteps, loss, n_updates))

# DataFrame
loss_updates_df = pd.DataFrame(loss_updates, columns=['timesteps', 'loss', 'n_updates'])

# Merge 
merged_df = pd.merge(csv_data, loss_updates_df, on='timesteps', how='left')

# Save
updated_csv_path = 'DQN\mario_rl\dqn\metrics\updated_dqn_metrics.csv'
merged_df.to_csv(updated_csv_path, index=False)

updated_csv_path
