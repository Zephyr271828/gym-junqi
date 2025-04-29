from typing import Union
from gym_junqi.custom_board import custom_board

"""
This file contains all the constants used throughout
the Junqi environment.
"""
import random
""" PATHS """
PATH_TO_SOUNDS = "sounds/"
PATH_TO_BOARD = "images_junqi/board/"
PATH_TO_BLACK = "images_junqi/black_pieces/"
PATH_TO_RED = "images_junqi/red_pieces/"
PATH_TO_UNKNOWN = "images_junqi/unknown_pieces/"

""" PYGAME """
# TODO: Change it
WINDOW_WIDTH = 521
WINDOW_HEIGHT = 896
FPS = 20
COUNT = 10

""" POINTS """
# Reference: https://max.book118.com/html/2017/0314/95322312.shtm
PIECE_POINTS = [
    0.,                     # EMPTY: No point for empty grid
    1000.,                  # FlAG: Priceless for the flag
    17.,                    # FIELD_MARSHAL: 10.0 points
    12.,                    # GENERAL: 12.0 points
    8., 8.,                  # ADVISOR: major_general points
    5., 5.,                  # BRIGADIER: 5.0 points
    4., 4.,                  # COLONEL: 4.0 points
    3., 3., 3.,               # ENGINEER: 3.0 points
    3., 3., 3.,               # LANDMINE: 3.0 points
    2., 2.,                  # MAJOR: 2.0 points
    0.8, 0.8, 0.8,            # CAPTAIN: 0.8 points
    0.2, 0.2, 0, 2,            # LIEUTENANT: 0.2 points
    6., 6.,                  # BOMB: 6.0 points
    4.,                     # UNKNOWN: 4. points
]

ILLEGAL_MOVE = -20.
WIN = PIECE_POINTS[1]
LOSE = -PIECE_POINTS[1]

""" PIECE """
ALLY = 1
ENEMY = -1

PIECE_CNT = 25              # Total number of pieces in each side

# Piece IDs
EMPTY = 0
FLAG = 1
FIELD_MARSHAL = 2
GENERAL = 3
MAJOR_GENERAL_1 = 4
MAJOR_GENERAL_2 = 5
BRIGADIER_1 = 6
BRIGADIER_2 = 7
COLONEL_1 = 8
COLONEL_2 = 9
ENGINEER_1 = 10
ENGINEER_2 = 11
ENGINEER_3 = 12
LANDMINE_1 = 13
LANDMINE_2 = 14
LANDMINE_3 = 15
MAJOR_1 = 16
MAJOR_2 = 17
CAPTAIN_1 = 18
CAPTAIN_2 = 19
CAPTAIN_3 = 20
LIEUTENANT_1 = 21
LIEUTENANT_2 = 22
LIEUTENANT_3 = 23
BOMB_1 = 24
BOMB_2 = 25
<<<<<<< HEAD
HIDDEN = 26
=======
UNKNOWN = 26
>>>>>>> 693ec261bb012458b360dbc63f5c981ee51b0bd1


PIECE_ID_TO_NAME = [
    "EMPTY", "FLAG", "FIELD_MARSHAL", "GENERAL",
    "MAJOR_GENERAL_1", "MAJOR_GENERAL_2", "BRIGADIER_1",
    "BRIGADIER_2", "COLONEL_1", "COLONEL_2",
    "ENGINEER_1", "ENGINEER_2", "ENGINEER_3",
    "LANDMINE_1", "LANDMINE_2", "LANDMINE_3",
    "MAJOR_1", "MAJOR_2", "CAPTAIN_1",
    "CAPTAIN_2", "CAPTAIN_3", "LIEUTENANT_1",
    "LIEUTENANT_2", "LIEUTENANT_3", "BOMB_1",
    "BOMB_2", "UNKNOWN"
]

# Piece Movement Offsets
ORTHOGONAL = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIAGONAL = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

# Piece States
RED = 0
BLACK = 1
DEAD = 0
ALIVE = 1
UNKNOWN = 0
KNOWN = 1

# Piece Size
# TODO: Change it
PIECE_WIDTH = 64
PIECE_HEIGHT = 32
MINI_PIECE_WIDTH = 12
MINI_PIECE_HEIGHT = 6

""" BOARD """
# Board Size
# TODO: Change it
BOARD_WIDTH = 512
BOARD_HEIGHT = 896
# BOARD_Y_OFFSET = (WINDOW_HEIGHT/2 - BOARD_HEIGHT/2)
BOARD_Y_OFFSET = 0

# Board Dimension
BOARD_ROWS = 12
BOARD_COLS = 5

# 边的情况（60个节点互相之间的情况）
BOARD_EDGES = [[0] * 60 for _ in range(60)]

# NOTE convert 2D coordinates to 1D index
def convert2idx(*args):
    if isinstance(args[0], list) or isinstance(args[0], tuple):
        (r, c) = args[0]
    else:
        r, c = args[0], args[1]
    if r < 0 or r >= BOARD_ROWS or c < 0 or c >= BOARD_COLS:
        return -1
    return r * BOARD_COLS + c   

# NOTE add a bidirectional path between pos1 and pos2 and given value
def add_road(pos1, pos2, value):
    BOARD_EDGES[convert2idx(pos1)][convert2idx(pos2)] = value
    BOARD_EDGES[convert2idx(pos2)][convert2idx(pos1)] = value

# HEADQUARTERS coordinates 大本营位置
HEADQUARTERS_ALLY_2D = [(11, 1), (11, 3)]
HEADQUARTERS_ENEMY_2D = [(0, 1), (0, 3)]
HEADQUARTERS_ALLY_1D = [convert2idx(each) for each in HEADQUARTERS_ALLY_2D]
HEADQUARTERS_ENEMY_1D = [convert2idx(each) for each in HEADQUARTERS_ENEMY_2D]

# CAMPSITE coordinates 行营位置
CAMP_ALLY = [(7, 1), (7, 3), (8, 2), (9, 1), (9, 3)]
CAMP_ENEMY = [(2, 1), (2, 3), (3, 2), (4, 1), (4, 3)]
CAMP_ALLY_1D = [convert2idx(each) for each in CAMP_ALLY]
CAMP_ENEMY_1D = [convert2idx(each) for each in CAMP_ENEMY]

# 0: no edge, 1: road, 2: railroad
# 以下定义所有的road
# NOTE add horizontal and vertical roads
for r in range(BOARD_ROWS):
    for c in range(BOARD_COLS):
        if c < BOARD_COLS - 1:
            add_road((r, c), (r, c+1), 1)
        if r < BOARD_ROWS - 1:
            add_road((r, c), (r+1, c), 1)
add_road((5, 1), (6, 1), 0)
add_road((5, 3), (6, 3), 0)
# NOTE add diagonal roads
for r in [2, 4, 7, 9]:
    for c in [1, 3]:
        add_road((r, c), (r+1, c+1), 1)
        add_road((r, c), (r+1, c-1), 1)
        add_road((r, c), (r-1, c+1), 1)
        add_road((r, c), (r-1, c-1), 1)
        
# NOTE add rail roads
# NOTE horizontal
for r in [1, 5, 6, 10]:
    for c in range(BOARD_COLS - 1):
        add_road((r, c), (r, c+1), 2)
# NOTE vertical
for r in range(1, BOARD_ROWS - 2):
    for c in [0, 4]:
        add_road((r, c), (r+1, c), 2)
add_road((5, 2), (6, 2), 2)

def random_formation():
    """
    Generate a random formation of pieces on the board.
    """
    formation = [None] * 60

    # 固定位置的行营，不能放任何东西
    forced_zero = set([convert2idx(r, c) for r in [2, 4, 7, 9] for c in [1, 3]])
    forced_zero.add(convert2idx(3, 2))
    forced_zero.add(convert2idx(8, 2))
    for idx in forced_zero:
        formation[idx] = 0

    # 上半棋盘只能是敌方棋子
    neg_positions = [i for i in range(0, 30) if i not in forced_zero]
    # 下半棋盘只能是我方棋子
    pos_positions = [i for i in range(30, 60) if i not in forced_zero]

    # 定义敌方25 个子和我方25 个
    negatives = [-i for i in range(1, 26)]  # -1, -2, ..., -25
    positives = [i for i in range(1, 26)]     # 1, 2, ..., 25

    # 处理上半部分特殊要求：行营中，一个必须为 -1（军棋），另一个必须为排长或者地雷
    special_S_neg = [-21, -22, -23, -13, -14, -15]
    if random.choice([True, False]):
        formation[1] = -1
        other_neg_index = 3
    else:
        formation[3] = -1
        other_neg_index = 1
    chosen_special_neg = random.choice(special_S_neg)
    formation[other_neg_index] = chosen_special_neg
    # 从敌方棋子移除已经用掉的两个子
    negatives.remove(-1)
    negatives.remove(chosen_special_neg)
    # 从可用位置中移除两个大本营
    neg_positions.remove(1)
    neg_positions.remove(3)

    # 对剩下的分配，需满足：
    # 1. 如果是地雷，则位置必须在最后两排。
    # 2. 第一排不能放炸弹
    valid_neg = False
    for _ in range(1000):
        perm = negatives[:]
        random.shuffle(perm)
        candidate_neg = {}
        valid = True
        for pos, num in zip(sorted(neg_positions), perm):
            if num in {-13, -14, -15} and pos >= 10:
                valid = False
                break
            if 25 <= pos <= 29 and num in {-24, -25}:
                valid = False
                break
            candidate_neg[pos] = num
        if valid:
            valid_neg = True
            break
    if not valid_neg:
        raise ValueError("无法为负数部分分配满足条件的数字")
    for pos, num in candidate_neg.items():
        formation[pos] = num

    # 下半部分同样处理
    special_S_pos = [21, 22, 23, 13, 14, 15]
    if random.choice([True, False]):
        formation[56] = 1
        other_pos_index = 58
    else:
        formation[58] = 1
        other_pos_index = 56
    chosen_special_pos = random.choice(special_S_pos)
    formation[other_pos_index] = chosen_special_pos
    positives.remove(1)
    positives.remove(chosen_special_pos)
    pos_positions.remove(56)
    pos_positions.remove(58)

    valid_pos = False
    for _ in range(1000):
        perm = positives[:]
        random.shuffle(perm)
        candidate_pos = {}
        valid = True
        for pos, num in zip(sorted(pos_positions), perm):
            if num in {13, 14, 15} and not (50 <= pos <= 59):
                valid = False
                break
            if 30 <= pos <= 34 and num in {24, 25}:
                valid = False
                break
            candidate_pos[pos] = num
        if valid:
            valid_pos = True
            break
    if not valid_pos:
        raise ValueError
    for pos, num in candidate_pos.items():
        formation[pos] = num

    # Reshape to 2D board
    formation_2d = []
    for i in range(12):
        row = formation[i * 5:(i + 1) * 5]
        formation_2d.append(row)
    # NOTE custom board state for test
    # formation_2d = custom_board
    return formation_2d


INITIAL_BOARD = random_formation()

""" OTHER """
# Maybe useless in Junqi
MAX_REP = 12         # number that is large enough to cover board width/height
TOTAL_POS = BOARD_ROWS * BOARD_COLS

""" Piece Coordinate Conversion """
# TODO: Change it
COOR_X_DELTA = 107
COOR_Y_DELTA = 65
COOR_X_OFFSET = 10
COOR_Y_OFFSET = 15
COOR_RIVER_OFFSET = 40


if __name__ == "__main__":
    # Visualize the board edges
    # This is for debugging purpose only
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 12))
    ax = plt.gca()

    positions = {}
    n_rows = 12
    n_cols = 5
    for i in range(60):
        row = i // n_cols
        col = i % n_cols
        x = col
        y = n_rows - 1 - row
        positions[i] = (x, y)
    for i, (x, y) in positions.items():
        ax.plot(x, y, 'ko', markersize=8)
        ax.text(x, y, str(i), fontsize=8, ha='center',
                va='center', color='white')
    for i in range(60):
        for j in range(i + 1, 60):
            edge_type = BOARD_EDGES[i][j]
            if edge_type != 0:
                x_values = [positions[i][0], positions[j][0]]
                y_values = [positions[i][1], positions[j][1]]
                if edge_type == 1:
                    color = 'red'
                elif edge_type == 2:
                    color = 'blue'
                ax.plot(x_values, y_values, color=color, linewidth=1)

    ax.set_xlim(-1, n_cols)
    ax.set_ylim(-1, n_rows)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.savefig('board_edges.png')
