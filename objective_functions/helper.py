from objective_functions import manhattan_distance


def find_neighbors(head_coords, body_coords, walls_coords,snake_direction, grid_height, grid_width):
   
    
    x, y = head_coords
    potential_neighbors = [
        (x - 1, y) if x - 1 >= 0 else None,      # Left
        (x + 1, y) if x + 1 < grid_width else None, # Right
        (x, y + 1) if y + 1 < grid_height else None, # Up
        (x, y - 1) if y - 1 >= 0 else None      # Down
    ]
    
    # Use a list comprehension for a safe and clean filter
    valid_neighbors = [
        n for n in potential_neighbors 
        if n is not None and (n not in body_coords and n not in walls_coords)
    ]

    return valid_neighbors




def get_turn_direction(snake_head: tuple, snake_direction: str, best_move: tuple) -> str:
    """
    Determines if the snake should go straight, turn left, or turn right.

    Args:
        snake_head: A tuple (x, y) for the snake's head position.
        snake_direction: A string ('UP', 'DOWN', 'LEFT', 'RIGHT') for the current direction.
        best_move: A tuple (x, y) for the target next position.

    Returns:
        A string: 'straight', 'left', or 'right'.
    """
    # Vector mappings for each direction (assuming y increases upwards)
    direction_vectors = {
        'UP':    (0, 1),
        'DOWN':  (0, -1),
        'LEFT':  (-1, 0),
        'RIGHT': (1, 0)
    }

    # Get the vector for the current direction
    current_direction_vector = direction_vectors[snake_direction]
    dx1, dy1 = current_direction_vector

    # Calculate the vector for the best move relative to the head
    move_vector = (best_move[0] - snake_head[0], best_move[1] - snake_head[1])
    dx2, dy2 = move_vector

    # Calculate the 2D cross product to determine the turn
    # cross_product > 0: counter-clockwise turn (left)
    # cross_product < 0: clockwise turn (right)
    # cross_product = 0: vectors are parallel (straight)
    cross_product = dx1 * dy2 - dy1 * dx2

    if cross_product > 0:
        return 'right'
    elif cross_product < 0:
        return 'left'
    else:
        return 'straight'
    
def check_body_overlap(neighboring_points: list, body_coords: list, wall_coords: list):
    """Counts how many of a point's neighbors are occupied by the snake's body."""
    return sum(1 for pt in neighboring_points if (pt in body_coords or pt in wall_coords))



def find_next_move(grid_height, grid_width, food, walls, score, my_snake_direction, my_snake_body, enemy_snakes):
    nbrs = find_neighbors(my_snake_body[0], my_snake_body, list(walls), my_snake_direction, grid_height, grid_width)
  

    fruit_coords = list(food)[0]
    
    move_scores = {}
    for move in nbrs:
        if move != None:
            overlap = check_body_overlap(find_neighbors(move, my_snake_body, list(walls), my_snake_direction, grid_height, grid_width), my_snake_body, list(walls))
            move_scores[move] = {
                'dist': manhattan_distance.manhattan_distance(move, fruit_coords),
                'overlap_factor': overlap
            }


    
    
    keys_to_pop = []
    for key in move_scores.keys():
        if move_scores[key]['overlap_factor'] > 2:
            keys_to_pop.append(key)


    if len(keys_to_pop) != len(move_scores.keys()):
        for key in keys_to_pop:
            move_scores.pop(key) 
    # Return the key (the coordinate) with the minimum (distance, overlap) tuple
    try:
        return min(move_scores, key=lambda k: (move_scores[k]['dist'], move_scores[k]['overlap_factor']))
    
    except:
        return (0,0)



    



    
    