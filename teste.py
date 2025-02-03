import gym
from multi_agent_emergence_environments.mae_envs.envs.hide_and_seek import HideAndSeekEnv

# Inicialize o ambiente manualmente
env = HideAndSeekEnv()
obs = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # Ação aleatória para cada agente
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
env.close()
