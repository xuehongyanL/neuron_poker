"""
Usage:
  bench.py --epoch=<>
"""
from main import Runner
from docopt import docopt
import matplotlib.pyplot as plt

args = docopt(__doc__)
epoch = int(args['--epoch'])

leaderboard = {}

for i in range(epoch):
    runner = Runner(
        render=None,
        num_episodes=None,
        use_cpp_montecarlo=False,
        funds_plot=False
    )
    runner.bench()
    winner_name = runner.env.best_player.name
    leaderboard[winner_name] = leaderboard.get(winner_name, 0) + 1

    plt.close("all")
    print(f'Epoch {i+1} finished')
    print(leaderboard)

print('==================================')
print('Result')
print(leaderboard)
