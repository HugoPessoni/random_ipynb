import torch
import gym
from gym.wrappers import FrameStack, GrayScaleObservation, TransformObservation
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros import make
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from gym.wrappers.frame_stack import LazyFrames
import numpy as np
import pandas as pd
import os

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

# Classe de Callback para salvar métricas
class MetricsCallback(BaseCallback):
    def __init__(self):
        super(MetricsCallback, self).__init__()
        self.timesteps = []
        self.reward_mean = []
        self.loss_mean = []

    def _on_step(self) -> bool:
        if "infos" in self.locals:
            infos = self.locals["infos"]
            rewards = [info["episode"]["r"] for info in infos if "episode" in info]
            if rewards:
                self.timesteps.append(self.num_timesteps)
                self.reward_mean.append(np.mean(rewards))
                if "loss" in self.locals.get("train_infos", {}):
                    self.loss_mean.append(self.locals["train_infos"]["loss"])
                else:
                    self.loss_mean.append(0)
        return True

    def save_metrics(self, csv_path: str):
        metrics_df = pd.DataFrame({
            "timesteps": self.timesteps,
            "reward_mean": self.reward_mean,
            "loss_mean": self.loss_mean,
        })
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        metrics_df.to_csv(csv_path, index=False)
        print(f"Métricas salvas em {csv_path}")

# Inicializar o callback de métricas
metrics_callback = MetricsCallback()

# Treinamento com callback para logar métricas
model.learn(total_timesteps=2000000, callback=metrics_callback)

# Salvando o modelo
model.save("dqn_mario")

# Salvando métricas em CSV
csv_path = "metrics/dqn_metrics.csv"
metrics_callback.save_metrics(csv_path)
