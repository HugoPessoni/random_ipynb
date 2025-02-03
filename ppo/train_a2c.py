import matplotlib.pyplot as plt
import pandas as pd
import torch
from env import get_env
from callback import TrainAndLoggingCallback
from model import MarioNet
from pathlib import Path

from stable_baselines3 import A2C

# Model Param
CHECK_FREQ_NUMB = 10000
TOTAL_TIMESTEP_NUMB = 6000000
LEARNING_RATE = 0.0007 # A2C needs higher learning rate
ENT_COEF = 0.02
N_STEPS = 8 # Shorter rollouts for A2C
GAMMA = 0.99

VF_COEF = 0.5  # Value Function coefficient
RMS_PROP_EPS = 1e-5  # RMSprop epsilon
MAX_GRAD_NORM = 0.5  # Maximum gradient norm

# Test Param
EPISODE_NUMBERS = 20
MAX_TIMESTEP_TEST = 1000

def linear_schedule(initial_value: float):
    def func(progress_remaining: float) -> float:
        return progress_remaining * initial_value
    return func

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
    optimizer_class=torch.optim.RMSprop,
    optimizer_kwargs=dict(eps=RMS_PROP_EPS, alpha=0.99, weight_decay=0.0),
)

save_dir = Path('./model_a2c')
save_dir.mkdir(parents=True, exist_ok=True)
reward_log_path = (save_dir / 'reward_log.csv')

with open(reward_log_path, 'a') as f:
    print('timesteps,reward,best_reward', file=f)

model = A2C('CnnPolicy', 
            env, 
            verbose=0, 
            policy_kwargs=policy_kwargs,
            tensorboard_log=save_dir,
            learning_rate=linear_schedule(LEARNING_RATE),
            n_steps=N_STEPS, 
            gamma=GAMMA,
            ent_coef=ENT_COEF,
            vf_coef=VF_COEF,
            max_grad_norm=MAX_GRAD_NORM,
            rms_prop_eps=RMS_PROP_EPS)
# model = A2C.load(save_dir / 'best_model_2000000.zip', env=env)

callback = TrainAndLoggingCallback(check_freq=CHECK_FREQ_NUMB, 
                                 save_path=save_dir, 
                                 episode_numbers=EPISODE_NUMBERS, 
                                 env=env, 
                                 max_timestep_test=MAX_TIMESTEP_TEST, 
                                 model=model, 
                                 total_timesteps=TOTAL_TIMESTEP_NUMB, 
                                 reward_log_path=reward_log_path)


model.learn(total_timesteps=TOTAL_TIMESTEP_NUMB, callback=callback)
