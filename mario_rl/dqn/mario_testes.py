import torch
import gym
from gym.wrappers import FrameStack, GrayScaleObservation, TransformObservation
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros import make
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from gym.wrappers.frame_stack import LazyFrames
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Função para converter LazyFrames para numpy
def lazyframes_to_numpy(lazyframes):
    if isinstance(lazyframes, gym.wrappers.frame_stack.LazyFrames):
        return np.array(lazyframes)
    return lazyframes

# Função para criar o ambiente com wrappers necessários
def create_env():
    env = make("SuperMarioBros-1-1-v0")  # Criação do ambiente
    env = JoypadSpace(env, [["right"], ["right", "A"]])  # Ações simplificadas
    env = GrayScaleObservation(env)  # Escala de cinza
    env = TransformObservation(env, lambda obs: obs.squeeze(-1) if obs.shape[-1] == 1 else obs)
    env = FrameStack(env, num_stack=4)  # Empilha 4 frames para contexto temporal
    return env

# Envolver com Monitor e DummyVecEnv para compatibilidade com stable-baselines3
env = DummyVecEnv([lambda: Monitor(create_env())])

# Configurar o modelo DQN
model = DQN(
    policy="CnnPolicy",  # Política baseada em CNN
    env=env,
    learning_rate=0.00025,
    buffer_size=100000,  # Tamanho do replay buffer
    learning_starts=5000,  # Passos antes de iniciar o treinamento
    batch_size=32,
    tau=0.1,
    gamma=0.99,
    target_update_interval=10000,  # Atualização da rede-alvo a cada 10k steps
    train_freq=4,  # Frequência de treinamento
    gradient_steps=1,  # Gradiente por passo de treino
    exploration_fraction=0.1,
    exploration_final_eps=0.1,
    verbose=1,  # Verbosidade para acompanhar progresso
    tensorboard_log="./mario_dqn_tensorboard/",  # Log para tensorboard
    device="cuda" if torch.cuda.is_available() else "cpu",
)

# Treinamento
model.learn(total_timesteps=40000)  # Número total de timesteps para treino

# Salvando o modelo
model.save("dqn_mario")

# Função para plotar métricas de treinamento a partir de um CSV
def plot_metrics(csv_file, output_dir):
    data = pd.read_csv(csv_file)

    # Plotar recompensas médias
    plt.figure(figsize=(10, 6))
    plt.plot(data['timesteps'], data['reward_mean'], label='Recompensa Média')
    plt.xlabel('Timesteps')
    plt.ylabel('Recompensa Média')
    plt.title('Recompensa Média durante o Treinamento')
    plt.legend()
    plt.savefig(f"{output_dir}/reward_plot.png")

    # Plotar perda média
    plt.figure(figsize=(10, 6))
    plt.plot(data['timesteps'], data['loss_mean'], label='Perda Média', color='orange')
    plt.xlabel('Timesteps')
    plt.ylabel('Perda Média')
    plt.title('Perda Média durante o Treinamento')
    plt.legend()
    plt.savefig(f"{output_dir}/loss_plot.png")

