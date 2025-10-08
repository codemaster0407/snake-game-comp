import random
from collections import deque
from snake.logic import GameState, Turn, Snake, Direction
from objective_functions import helper
"""
Your mission, should you choose to accept it, is to write the most cracked snake AI possible.

All the info you'll need to do this is in the GameState and Snake classes in snake/logic.py

Below is all of the data you'll need, and some small examples that you can uncomment and use if you want :)

"""


def myAI(state: GameState) -> Turn:

    # ======================================
    # =         Some Useful data.          =
    # ======================================

    grid_width: int = state.width
    grid_height: int = state.height
    food: set = state.food
    walls: set = state.walls
    score: int = state.score
    my_snake: Snake = state.snake
    my_snake_direction: Direction = Direction(state.snake.direction)
    my_snake_body: list = list(state.snake.body)
    enemy_snakes = state.enemies
    snakes_list = []


    for snake in enemy_snakes:
        snakes_list.append(list(snake.body))
    # print(snakes_list)

    
    # you may also find the get_next_head() method of the Snake class useful!
    # this tells you what position the snake's head will end up in for each of the moves
    # you can then check for collisions, food etc
    straight = my_snake.get_next_head(Turn.STRAIGHT)
    left = my_snake.get_next_head(Turn.LEFT)
    right = my_snake.get_next_head(Turn.RIGHT)

    
    next_move = helper.find_next_move(grid_height, grid_width, food, walls, score, my_snake_direction, my_snake_body, snakes_list)
    if next_move == (0,0):
        return random.choice(list(Turn))
    if straight == next_move:
        return Turn.STRAIGHT
    elif left == next_move:
        return Turn.LEFT 
    else:
        return Turn.RIGHT
    # ======================================
    # =         Your Code Goes Here        =
    # ======================================
   
    # return random.choice(list(Turn))

    # ======================================
    # =       Try out some examples!       =
    # ======================================

    # from examples.dumbAI import dumbAI
    # return dumbAI(state)

    #from examples.smartAI import smartAI
    #return smartAI(state)
