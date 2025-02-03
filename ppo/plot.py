import pandas as pd

reward_log = pd.read_csv("model/reward_log.csv", index_col='timesteps')
plot = reward_log.plot()
plot.figure.savefig('./model/reward_plot.png')
