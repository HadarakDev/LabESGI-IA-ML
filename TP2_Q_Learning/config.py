import numpy as np


item_map = np.array((["M", "0", "C2"], ["C2", "P", "C3"]))
position_map = np.array(([(100, 100), (500, 100), (900, 100)], [(100, 500), (500, 500), (900, 500)]))
score_map = [
    [0, 1, 0],
    [2, -10, 10],
    [0, 0, 0]
]

actions = [[-1, 0], # Up
            [1, 0], # Down
            [0, -1], # Left
            [0, 1]] # right


