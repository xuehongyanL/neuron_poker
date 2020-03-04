from stats.func import *

import matplotlib.pyplot as plt
import numpy as np


def draw(x_plots, y_plots, color):
    plot_upper = [getMaxVal(game) for game in y_plots]
    plot_lower = [getMinVal(game) for game in y_plots]
    plot_avg = [getAvgVal(game) for game in y_plots]
    plot_diff = [getDiffVal(game) for game in y_plots]
    plt.plot(x_plots, plot_lower, color=color)
    plt.plot(x_plots, plot_upper, color=color)
    plt.plot(x_plots, plot_avg, color=color, linewidth=4)
    plt.plot(x_plots, plot_diff, color=color)

    val_array = np.array([(getVal(game[0]), getVal(game[1])) for game in y_plots]).flatten()
    return {
        'avg': np.mean(val_array),
        'std': np.std(val_array, ddof=1)
    }
