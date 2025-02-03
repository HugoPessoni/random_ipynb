import matplotlib.pyplot as plt
import pandas as pd
from env import get_env
from callback import TrainAndLoggingCallback
from model import MarioNet
from pathlib import Path

from stable_baselines3 import PPO

# Model Param
CHECK_FREQ_NUMB = 10000
TOTAL_TIMESTEP_NUMB = 5000000
LEARNING_RATE = 0.0001
GAE = 1.0
ENT_COEF = 0.01
N_STEPS = 512
GAMMA = 0.9
BATCH_SIZE = 64
N_EPOCHS = 10

# Test Param
EPISODE_NUMBERS = 20
MAX_TIMESTEP_TEST = 1000


def display_all_frame(state):
    plt.figure(figsize=(16,16))
    for idx in range(state.shape[3]):
        plt.subplot(1,4,idx+1)
        plt.imshow(state[0][:,:,idx])
    plt.show()

STAGE_NAME = 'SuperMarioBros-1-1-v3'
env = get_env(STAGE_NAME)

env.reset()
state, reward, done, info = env.step([0])

policy_kwargs = dict(
    features_extractor_class=MarioNet,
    features_extractor_kwargs=dict(features_dim=512),
)

save_dir = Path('./model_retangular')
save_dir.mkdir(parents=True, exist_ok=True)
reward_log_path = (save_dir / 'reward_log.csv')

with open(reward_log_path, 'a') as f:
    print('timesteps,reward,best_reward', file=f)

model = PPO('CnnPolicy', env, verbose=0, policy_kwargs=policy_kwargs, tensorboard_log=save_dir, learning_rate=LEARNING_RATE, n_steps=N_STEPS,
              batch_size=BATCH_SIZE, n_epochs=N_EPOCHS, gamma=GAMMA, gae_lambda=GAE, ent_coef=ENT_COEF)

callback = TrainAndLoggingCallback(check_freq=CHECK_FREQ_NUMB, save_path=save_dir, episode_numbers=EPISODE_NUMBERS, env=env, max_timestep_test=MAX_TIMESTEP_TEST, model=model, total_timesteps=TOTAL_TIMESTEP_NUMB, reward_log_path=reward_log_path)

model.learn(total_timesteps=TOTAL_TIMESTEP_NUMB, callback=callback)
