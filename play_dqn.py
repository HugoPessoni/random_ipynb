import torch
import gym
from gym.wrappers import FrameStack, GrayScaleObservation, TransformObservation, RecordVideo
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros import make
from stable_baselines3 import DQN
import numpy as np
import os


# Função para criar o ambiente com wrappers necessários
def create_env(video_folder=None):
    env = make("SuperMarioBros-1-1-v3")  # Criação do ambiente
    env = JoypadSpace(env, [["right"], ["right", "A"]])  # Ações simplificadas
    env = GrayScaleObservation(env)  # Escala de cinza
    env = TransformObservation(env, lambda obs: obs.squeeze(-1) if obs.shape[-1] == 1 else obs)
    env = FrameStack(env, num_stack=4)  # Empilha 4 frames para contexto temporal
    if video_folder:
        env = RecordVideo(env, video_folder=video_folder, episode_trigger=lambda x: True)
    return env


# Função para jogar utilizando o modelo salvo
def play(model_path, video_folder="videos/"):
    from gym.wrappers.frame_stack import LazyFrames

    # Garantir que a pasta de vídeos exista
    os.makedirs(video_folder, exist_ok=True)

    # Carregar modelo treinado
    model = DQN.load(model_path)  # Carregar modelo salvo do arquivo .zip
    
    # Criar o ambiente configurado como no treinamento, com gravação de vídeo
    env = create_env(video_folder=video_folder)

    # Resetar o ambiente
    state = env.reset()
    done = False

    while not done:
        # Garantir que o estado seja um array numpy
        if isinstance(state, LazyFrames):
            state = np.array(state)

        # Prever ação e converter para inteiro
        action, _ = model.predict(state)
        action = action.item()  # Converte para escalar

        # Realizar a ação no ambiente
        state, reward, done, info = env.step(action)

    # Fechar o ambiente
    env.close()
    print(f"Vídeo salvo na pasta: {video_folder}")


# Jogar utilizando o modelo salvo e gerar vídeo
if __name__ == "__main__":
    play("DQN\mario_rl\dqn\models\dqn_mario.zip", video_folder="mario_videos/")
