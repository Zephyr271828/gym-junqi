from gym.envs.registration import register

register(
    id='junqi-v0',
    entry_point='gym_junqi.envs:JunQiEnv',
)
