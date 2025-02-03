import gym_super_mario_bros
from gym.wrappers import GrayScaleObservation
from nes_py.wrappers import JoypadSpace
from reward import CustomRewardAndDoneEnv
from preprocess import SkipFrame, ResizeEnv
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

def get_env(stage_name):
    MOVEMENT = [['left', 'A'], ['right', 'B'], ['right', 'A', 'B']]
    env = gym_super_mario_bros.make(stage_name)
    env = JoypadSpace(env, MOVEMENT)
    env = CustomRewardAndDoneEnv(env)
    env = SkipFrame(env, skip=4)
    env = GrayScaleObservation(env, keep_dim=True)
    env = ResizeEnv(env, size=84)
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, 4, channels_order='last')
    
    
    return env