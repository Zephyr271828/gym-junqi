import os

import pkg_resources
import numpy as np
import pygame

from gym_junqi.utils import move_to_action_space, is_ally
from gym_junqi.constants import (
    ORTHOGONAL, DIAGONAL,  # ELEPHANT_MOVE, HORSE_MOVE,    # piece moves
    BOARD_ROWS, BOARD_COLS,                             # board specs
    # PALACE_ALLY_ROW, PALACE_ENEMY_ROW, PALACE_COL,      # palace bound
    # RIVER_LOW, RIVER_HIGH,                              # river bound
    MAX_REP,                                            # repetition bound
    BLACK, ALIVE, ALLY, ENEMY,                          # piece states
    # board coordinate
    COOR_X_DELTA, COOR_Y_DELTA, COOR_X_OFFSET, COOR_Y_OFFSET,
    PIECE_WIDTH, PIECE_HEIGHT,                          # piece sizes
    MINI_PIECE_WIDTH, MINI_PIECE_HEIGHT,                # mini piece sizes
    PATH_TO_BLACK, PATH_TO_RED,                         # file paths to pieces
    EMPTY, GENERAL,                                     # piece IDs
    BOARD_Y_OFFSET                                      # board y offset
)


class Piece:
    """
    A base class for all Xiangqi pieces

    All pieces have the following:

        Attributes:
        - color: red or black
        - position: (row, column) coordinate
        - state: alive or dead (in game or out of game)
        - image: PyGame image object used when rendering

        Methods:
        - move(self): make allowed movements
    """

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.state = ALIVE
        self.legal_moves = None
        self.piece_width = PIECE_WIDTH
        self.piece_height = PIECE_HEIGHT
        self.mini_piece_width = MINI_PIECE_WIDTH
        self.mini_piece_height = MINI_PIECE_HEIGHT
        self.basic_image = None
        self.select_image = None
        self.mini_image = None
        self.move_sound = None

    def move(self, new_row, new_col):
        """
        Take one move among given piece's allowed moves
        Update piece's coordinates internally
        """
        if self.move_sound is not None:
            self.move_sound.play()
        self.row = new_row
        self.col = new_col

    def get_pygame_coor(self):
        x = self.col*COOR_X_DELTA + COOR_X_OFFSET
        y = self.row*COOR_Y_DELTA + COOR_Y_OFFSET + BOARD_Y_OFFSET

        # 处理河的偏移
        if self.row > 5:
            y += 120

        return (x, y)

    def load_image(self, filename: str, piece_width, piece_height):
        if self.color == BLACK:
            file_path = PATH_TO_BLACK
        else:
            file_path = PATH_TO_RED

        target_file = os.path.join(file_path, filename)
        target_file = pkg_resources.resource_filename(__name__, target_file)
        image = pygame.image.load(target_file).convert_alpha()
        image = pygame.transform.scale(
            image, (piece_width, piece_height)
        )
        return image

    def set_basic_image(self):
        filename = self.name + ".png"
        self.basic_image = (self.load_image(filename,
                            self.piece_width, self.piece_height))

    def set_select_image(self):
        # 1. 先加载基础图片
        filename = self.name + ".png"
        base_image = self.load_image(
            filename, self.piece_width, self.piece_height)

        # 2. 创建一个副本来绘制选择框
        selected_image = base_image.copy()

        # 3. 获取图像尺寸
        width, height = selected_image.get_size()

        # 4. 定义角落框的颜色和尺寸
        color = (190, 30, 20)
        line_width = 8
        corner_len = 10

        # 5. 使用 pygame.draw 画出四个角落
        # 左上
        pygame.draw.line(selected_image, color, (0, 0),
                         (corner_len, 0), line_width)
        pygame.draw.line(selected_image, color, (0, 0),
                         (0, corner_len), line_width)
        # 右上
        pygame.draw.line(selected_image, color,
                         (width - corner_len, 0), (width, 0), line_width)
        pygame.draw.line(selected_image, color, (width - 1, 0),
                         (width - 1, corner_len), line_width)
        # 左下
        pygame.draw.line(selected_image, color, (0, height -
                         corner_len), (0, height), line_width)
        pygame.draw.line(selected_image, color, (0, height - 1),
                         (corner_len, height - 1), line_width)
        # 右下
        pygame.draw.line(selected_image, color, (width - 1,
                         height - corner_len), (width - 1, height), line_width)
        pygame.draw.line(selected_image, color, (width - corner_len,
                         height - 1), (width, height - 1), line_width)

        print(f"{self.name} 被选中，添加四角选择框样式")
        self.select_image = selected_image

    def set_mini_image(self):
        filename = self.name + ".png"
        self.mini_image = (self.load_image(filename,
                           self.mini_piece_width, self.mini_piece_height))

    def is_alive(self):
        return self.state

    # getters
    @property
    def coor(self):
        return (self.col, self.row)


def check_action(piece_id, orig_pos, cur_pos,
                 repeat, offset, i, state, actions):
    """
    This is general searching procedure. Given the following parameters,
    repeatedly search in the same direction until either end of the board
    or another piece is blocking.

    Parameters:
        piece_id (int): piece ID
        orig_pos (tuple(int)): original coordinate of the piece
        cur_pos (tuple(int)): current position in evaluation
        repeat (int): number of repetitions to perform this procedure
        offset (tuple(int)): coordinate offset towards current direction
        i (int): current iteration number
        state (numpy.ndarray): current environment state
        actions (numpy.ndarray): pool of possible actions
    return:
        Number of times repeated; This is used to find out the farthest
        possible position used for other conditional check.
    """
    r = cur_pos[0]
    c = cur_pos[1]

    if not is_ally(piece_id):
        sign = ENEMY
        piece_id *= ENEMY
    else:
        sign = ALLY

    for i in range(repeat):
        rb = 0 <= r < BOARD_ROWS
        cb = 0 <= c < BOARD_COLS

        if not rb or not cb:
            return i

        # if ally piece is located, can't go further
        if state[r][c] * sign > 0:
            break

        if check_flying_general(state, sign, piece_id, orig_pos, (r, c)):
            return 0

        action_idx = move_to_action_space(piece_id, orig_pos, (r, c))
        actions[action_idx] = 1

        if state[r][c] != 0:
            break

        r += offset[0]
        c += offset[1]

    return i + 1


class Flag(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Flag, self).__init__(color, row, col)
        self.name = "flag"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Flag
        """
        pass


class Field_Marshal(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Field_Marshal, self).__init__(color, row, col)
        self.name = "field_marshal"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Field Marshal
        """
        pass


class General(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(General, self).__init__(color, row, col)
        self.name = "general"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the General
        """
        pass


class Major_General(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Major_General, self).__init__(color, row, col)
        self.name = "major_general"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Major General
        """
        pass


class Brigadier_General(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Brigadier_General, self).__init__(color, row, col)
        self.name = "brigadier_general"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Brigadier
        """
        pass


class Colonel(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Colonel, self).__init__(color, row, col)
        self.name = "colonel"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Colonel
        """
        pass


class Engineer(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Engineer, self).__init__(color, row, col)
        self.name = "engineer"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Engineer
        """
        pass


class Landmine(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Landmine, self).__init__(color, row, col)
        self.name = "landmine"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Land Mine
        """
        pass


class Major(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Major, self).__init__(color, row, col)
        self.name = "major"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Major
        """
        pass


class Captain(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Captain, self).__init__(color, row, col)
        self.name = "captain"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Captain
        """
        pass


class Lieutenant(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Lieutenant, self).__init__(color, row, col)
        self.name = "lieutenant"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Lieutenant
        """
        pass


class Bomb(Piece):
    """
    """

    def __init__(self, color, row, col):
        super(Bomb, self).__init__(color, row, col)
        self.name = "bomb"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Bomb
        """
        pass
