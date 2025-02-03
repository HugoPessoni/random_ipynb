import pandas as pd
import matplotlib.pyplot as plt
import os

# Carregar o CSV atualizado
csv_path = 'DQN/mario_rl/dqn/metrics/updated_dqn_metrics.csv'
data = pd.read_csv(csv_path)

# Filtrar os dados para evitar valores ausentes
filtered_data = data.dropna(subset=["reward_mean"])
data["n_updates"] = data["n_updates"].interpolate()


# Criar o gráfico de linha
plt.figure(figsize=(20, 12))
plt.plot(data["n_updates"], data["timesteps"], label="Timesteps vs Número de Atualizações", color="green")
plt.ylabel("Timesteps")
plt.xlabel("Número de Atualizações")
plt.title("Timesteps por Número de Atualizações")
plt.legend()
plt.grid(True)

# Salvar o gráfico em um arquivo
output_file = "DQN/mario_rl/dqn/graphs/timesteps_vs_n_updates.png"
plt.savefig(output_file)

print(f"Gráfico salvo em {output_file}")