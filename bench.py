"""
Usage:
  bench.py --epoch=<>
"""
from docopt import docopt
import matplotlib.pyplot as plt

from main import Runner
from stats.func import *
from stats.draw import draw

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
        Custom_Lite(),
        Custom_Lite(),
        # Custom_Lite(),
        Custom_Ensemble(),
        Custom_Ensemble(),
        # Custom_Ensemble(),
        # Custom_Ensemble_EX(),
        # Custom_Ensemble_EX(),
        # Custom_Ensemble_EX(),
        RandomPlayer(),
        PRT(env=env),
    ]


leaderboard = {}
stats = []

for i in range(epoch):
    runner = Runner(
        render=None,
        num_episodes=None,
        use_cpp_montecarlo=False,
        funds_plot=False
    )
    env = runner.get_bench_env()
    players = init_players(env)
    runner.bench_interface(env, players)
    winner_name = runner.env.best_player.name
    leaderboard[winner_name] = leaderboard.get(winner_name, 0) + 1
    plt.close("all")

    print(f'Epoch {i + 1} finished')
    print(leaderboard)


    def find_PRT(plrs):
        for plr in plrs:
            if plr.name == 'Random_PRT':
                return plr.agent_obj


    stat = find_PRT(env.players).stat
    # for plr in stat:
    #     print(plr)
    stats.append(stat)

print('==================================')
print('Result')
print(leaderboard)

plot_x = list(range(epoch))
plots_ensemble = [list(filter(select(['Ensemble']), game)) for game in stats]
plots_ex = [list(filter(select(['EnsembleEX']), game)) for game in stats]
plots_random = [list(filter(select(['Random', 'Random_PRT']), game)) for game in stats]

print(draw(plot_x, plots_ensemble, 'r'))
print(draw(plot_x, plots_ex, 'g'))
print(draw(plot_x, plots_random, 'b'))

plt.show()
