import numpy as np

position_map = np.array(([(100, 100), (400, 100), (700, 100)],
                         [(100, 400), (400, 400), (700, 400)],
                         [(100, 700), (400, 700), (700, 700)]))

item_map = np.array((["M", "C1", "0"],
                     ["C2", "P", "0"],
                     ["0", "0", "C3"]))

score_map = [
    [0, 1, 0],
    [2, -10, 0],
    [0, 0, 10]
]

actions = [[-1, 0],  # Up
           [1, 0],  # Down
           [0, -1],  # Left
           [0, 1]]  # right

action_text = ["TOP", "BOT", "LEFT", "RIGHT"]
