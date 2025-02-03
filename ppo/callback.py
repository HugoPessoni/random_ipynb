import os
from stable_baselines3.common.callbacks import BaseCallback

class TrainAndLoggingCallback(BaseCallback):
    def __init__(self, check_freq, save_path, episode_numbers, env, max_timestep_test, model, total_timesteps, reward_log_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path
        self.episode_numbers = episode_numbers
        self.env = env
        self.max_timestep_test = max_timestep_test
        self.model = model
        self.total_timesteps = total_timesteps
        self.reward_log_path = reward_log_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = (self.save_path / 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

            total_reward = [0] * self.episode_numbers
            total_time = [0] * self.episode_numbers
            best_reward = 0

            for i in range(self.episode_numbers):
                state = self.env.reset()  # reset for each new trial
                done = False
                total_reward[i] = 0
                total_time[i] = 0
                while not done and total_time[i] < self.max_timestep_test:
                    action, _ = self.model.predict(state)
                    state, reward, done, info = self.env.step(action)
                    total_reward[i] += reward[0]
                    total_time[i] += 1

                if total_reward[i] > best_reward:
                    best_reward = total_reward[i]
                    best_epoch = self.n_calls

                state = self.env.reset()  # reset for each new trial

            print('time steps:', self.n_calls, '/', self.total_timesteps)
            print('average reward:', (sum(total_reward) / self.episode_numbers),
                  'average time:', (sum(total_time) / self.episode_numbers),
                  'best_reward:', best_reward)

            with open(self.reward_log_path, 'a') as f:
                print(self.n_calls, ',', sum(total_reward) / self.episode_numbers, ',', best_reward, file=f)

        return True