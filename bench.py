"""
Usage:
  bench.py --epoch=<>
"""
from main import Runner
from docopt import docopt
import matplotlib.pyplot as plt
from copy import deepcopy

from agents.agent_random import Player as RandomPlayer
from agents.agent_AI import AI_Player as Custom_Lite
from agents.agent_equity_ensemble import Player as Custom_Ensemble
from agents.agent_equity_ensemble_ex import Player as Custom_Ensemble_EX
from agents.agent_PRT_random import Player as PRT

# 需要临时注释掉/gym_env/env.py中plt.show()语句
# 以免每一场结束后弹出一个折线图表

args = docopt(__doc__)
epoch = int(args['--epoch'])

def init_players(env):
    return [
        # RandomPlayer(),
        # RandomPlayer(),
        # RandomPlayer(),
        # Custom_Lite(),
        # Custom_Lite(),
        # Custom_Lite(),
        Custom_Ensemble(),
        Custom_Ensemble(),
        # Custom_Ensemble(),
        Custom_Ensemble_EX(),
        Custom_Ensemble_EX(),
        # Custom_Ensemble_EX(),
        RandomPlayer(),
        PRT(env=env),
    ]
players = deepcopy(init_players)
leaderboard = {}

for i in range(epoch):
    runner = Runner(
        render=None,
        num_episodes=None,
        use_cpp_montecarlo=False,
        funds_plot=False
    )
    runner.bench_interface(players)
    winner_name = runner.env.best_player.name
    leaderboard[winner_name] = leaderboard.get(winner_name, 0) + 1
    plt.close("all")

    # if i%5 == 0:
    #     players = deepcopy(init_players)
    # else:
    #     players = [agent.agent_obj for agent in runner.env.players if agent.agent_obj.name == 'EnsembleEX']
    #     players.extend([Custom_Ensemble(),Custom_Ensemble(),Custom_Ensemble()])

    print(f'Epoch {i+1} finished')
    print(leaderboard)

print('==================================')
print('Result')
print(leaderboard)
