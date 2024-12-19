# Author: Ntalcme
# Start On: 18/12/2024 3:37 (Paris' hour)
# End on: 19/12/2024 20:52 (Paris' hour)
# Coding time : 8h35m (docstring was really boring)
# Project: Textual 2048 for School, 1st year

# NOTE : I forgot to create a repo for this that's why there is only 1 commit.

########## IMPORTS ##########
from copy import deepcopy
from typing import Literal
from constants_2048 import ConstantsOf2048
import json
import random
#############################

with open("game_texts.json", 'r', encoding='utf-8') as texts:
    game_texts = json.load(texts)

def create_grid(length: int, width: int) -> list[list[int]]:
    """
    Creates a grid of length x width.

    Args:
        length: length of each line in grid.
        width: length of each column in grid.

    Returns:
        list[list[int]]: Representation of an empty grid of length x width.
    """
    return [[ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE] * length for _ in range(width)]

def display_grid(grid: list[list[int]], cell_size: int) -> None:
    """
    Displays the grid in the console.

    Args:
        grid: the grid to be displayed.
        cell_size: The cell size of the grid.
    """
    horizontal_border = ConstantsOf2048.Display.CORNER + (
                ConstantsOf2048.Display.BAR * cell_size + ConstantsOf2048.Display.CORNER) * len(grid[0])
    empty_line = ConstantsOf2048.Display.BORDER + (
                ConstantsOf2048.Display.CELL_SPACE * cell_size + ConstantsOf2048.Display.BORDER) * len(grid[0])
    lines = [horizontal_border]
    for line in grid:
        line_content = ConstantsOf2048.Display.BORDER
        for cell in line:
            content = f'{cell:^{cell_size}}' if cell != ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE else ConstantsOf2048.Display.CELL_SPACE * cell_size
            line_content += content + ConstantsOf2048.Display.BORDER
        lines.append(empty_line)
        lines.append(line_content)
        lines.append(empty_line)
        lines.append(horizontal_border)
    print('\n'.join(lines))

def get_random_empty_cell_in_grid(grid: list[list[int]]) -> tuple[int, int]:
    """
    Get a random empty cell in the grid.

    Args:
        grid: the grid.

    Returns:
        tuple[int, int]: Coordinates of a random empty cell.
    """
    x, y = (random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1))
    while grid[x][y] != ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE:
        x, y = (random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1))

    return x, y

def generate_new_tile() -> Literal[2, 4]:
    """
    Generate a random number between 2 and 4 with 2048's probabilities.

    Returns:
        Literal[2, 4]: 2 or 4.
    """
    return 2 if random.random() < ConstantsOf2048.Gameplay.SPAWN_PROBABILITIES[2] else 4

def init_2048_grid(grid: list[list[int]]) -> list[list[int]]:
    """
    Initialize a 2048 grid.

    Args:
        grid: an empty 2048 grid.

    Returns:
        list[list[int]]: a starting 2048 grid.
    """
    new_grid = deepcopy(grid)
    x1, y1 = get_random_empty_cell_in_grid(grid)

    if random.choice((True, False)):
        x2, y2 = get_random_empty_cell_in_grid(grid)
        while (x2, y2) == (x1, y1):
            x2, y2 = get_random_empty_cell_in_grid(grid)
        first_choice = generate_new_tile()
        new_grid[x1][y1] = first_choice
        new_grid[x2][y2] = 2 if first_choice == 4 else generate_new_tile()

        return new_grid
    new_grid[x1][y1] = 2

    return new_grid

def grid_transposition(grid: list[list[int]]) -> list[list[int]]:
    """
    Transpose a grid.

    Args:
        grid: the grid.

    Returns:
        list[list[int]]: Transposed grid.
    """
    return [list(line) for line in zip(*grid)]

def grid_symmetry(grid: list[list[int]]) -> list[list[int]]:
    """
    Make a symmetry of the grid.

    Args:
        grid: the grid.

    Returns:
        list[list[int]]: the symmetry of the grid.
    """
    return [line[::-1] for line in grid]

def grid_orient(grid: list[list[int]], move: ConstantsOf2048.Gameplay.Controls) -> list[list[int]]:
    """
    Orient a grid according to the given move.
    Args:
        grid: the grid.
        move: the move.

    Returns:
        list[list[int]]: oriented grid according to the move.
    """
    transformations = {
        ConstantsOf2048.Gameplay.Controls.LEFT: lambda g: grid_symmetry(g),
        ConstantsOf2048.Gameplay.Controls.RIGHT: lambda g: g,
        ConstantsOf2048.Gameplay.Controls.UP: lambda g: grid_symmetry(grid_transposition(g)),
        ConstantsOf2048.Gameplay.Controls.DOWN: lambda g: grid_transposition(g)
    }

    return transformations.get(move, lambda g: g)(grid)

def index_last_not_empty_cell_in_list(line: list[int]) -> int | None:
    """
    Get the index of the last non-empty cell in the list.
    Empty cell is represented by 0.

    Args:
        line: the list which represents a line of a grid.

    Returns:
        int | None : None if the line is empty else index of the last non-empty cell.
    """
    for i in range(len(line) - 1, -1, -1):
        if line[i] != ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE:
            return i

def delete_space_in_list(line: list[int]) -> list[int]:
    """
    Delete space between all non-empty cells in the list.
    Empty cell is represented by 0.
    All non-empty cells will be at the end of the list.

    Args:
        line: a list which represents a line of a grid.

    Returns:
        list[int]: a list after deleting space between all non-empty cells.
    """
    new_line = line.copy()
    for i in range(len(new_line) - 1, -1, -1):
        if new_line[i] == ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE:
            index_number_to_move = index_last_not_empty_cell_in_list(new_line[0:i])
            if index_number_to_move is not None:
                new_line[i] = new_line[index_number_to_move]
                new_line[index_number_to_move] = ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE
    return new_line

def grid_fusion(grid: list[list[int]]) -> list[list[int]]:
    """
    Fusion in each line of grid two numbers if these numbers are equal and there is no space or only empty spaces between them.

    Args:
        grid: the grid.

    Returns:
        list[list[int]] : the grid after fusions.
    """
    new_grid = deepcopy(grid)
    for i in range(len(new_grid)):
        for j in range(len(new_grid[i]) - 1, -1, -1):
            new_grid[i] = delete_space_in_list(new_grid[i])
            if new_grid[i][j] != ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE and new_grid[i][j] == new_grid[i][j - 1]:
                new_grid[i][j] = new_grid[i][j] * 2
                new_grid[i][j - 1] = ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE
                new_grid[i] = delete_space_in_list(new_grid[i])
        new_grid[i] = delete_space_in_list(new_grid[i])
    return new_grid

def add_number(grid: list[list[int]]) -> list[list[int]]:
    """
    Add a random number (2 or 4) to the grid.

    Args:
        grid: the grid.

    Returns:
        list[list[int]]: the grid with its new number.
    """
    new_grid = deepcopy(grid)
    x, y = get_random_empty_cell_in_grid(grid)
    new_grid[x][y] = generate_new_tile()
    return new_grid

def is_valid_move(move:str) -> bool:
    """
    True if move is a valid 2048 move in this context.

    Args:
        move: the given move.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    for control in ConstantsOf2048.Gameplay.Controls:
        if move == control.value:
            return True
    return False

def get_valid_move(prompt:str = game_texts["ask_move"]) -> ConstantsOf2048.Gameplay.Controls:
    """
    Ask the user to enter a valid 2048 move.

    Args:
        prompt: a prompt for asking the user.

    Returns:
        ConstantsOf2048.Gameplay.Controls: a valid 2048 move.
    """
    print(game_texts["controls"])
    move = input(prompt).strip(' ')
    while not is_valid_move(move):
        print(game_texts["not_valid_move"])
        print(game_texts["end"])
        move = input(prompt).strip(' ')
    return ConstantsOf2048.Gameplay.Controls(move)

def make_move(grid: list[list[int]], move: ConstantsOf2048.Gameplay.Controls) -> list[list[int]]:
    """
    Make a 2048 move according to the given move.

    Args:
        grid: the grid.
        move: a valid 2048 move.

    Returns:
        list[list[int]]: a grid after making a move.
    """
    if move == ConstantsOf2048.Gameplay.Controls.UP:
        return grid_transposition(grid_symmetry((grid_fusion(grid_orient(grid, move)))))
    return grid_orient(grid_fusion(grid_orient(grid, move)), move)

def can_move(grid: list[list[int]]) -> bool:
    """
    True if a 2048 move can be made.

    Args:
        grid: the grid.

    Returns:
        bool: True if a 2048 move can be made.
    """
    for move in ConstantsOf2048.Gameplay.Controls:
        if make_move(grid, move) != grid:
            return True
    return False

def can_play(grid: list[list[int]]) -> bool:
    """
    True if the player can play the 2048 game.

    Args:
        grid: the grid.

    Returns:
        bool: True if the player can play the 2048 game.
    """
    return any(cel == ConstantsOf2048.Gameplay.EMPTY_CELL_VALUE for line in grid for cel in line) or can_move(grid)

def main():
    """
    Main function to play 2048 game.
    """
    grid_2048 = init_2048_grid(create_grid(4, 4))
    while can_play(grid_2048):
        display_grid(grid_2048, ConstantsOf2048.Display.CELL_SIZE)
        new_grid_2048 = make_move(grid_2048, get_valid_move())
        if new_grid_2048 != grid_2048:
            grid_2048 = add_number(new_grid_2048)
        else:
            grid_2048 = new_grid_2048
