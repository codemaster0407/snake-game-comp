from objective_functions import manhattan_distance


def find_neighbors(head_coords, body_coords, walls_coords,snake_direction, grid_height, grid_width):
    x, y = head_coords
    neighbors = [
        (x - 1, y) if x-1 >=0 else None,  # Left
        (x + 1, y) if x+1 < grid_width else None,  # Right
        (x, y + 1) if y+1< grid_height else None,  # Up
        (x,y - 1) if y-1 >=0 else None  #Down
    ]
    if str(snake_direction)== 'Direction.Up':
        neighbors.pop(3)
    
    if str(snake_direction) == 'Direction.Down':
        neighbors.pop(2)
    
    if str(snake_direction) == 'Direction.Right':
        neighbors.pop(0)
    
    if str(snake_direction) == 'Direction.Left':
        neighbors.pop(1)
    
    if None in neighbors:
        neighbors.remove(None)

    for nbr in neighbors:
        if nbr in body_coords:
            neighbors.remove(nbr)
        if nbr in walls_coords:
            neighbors.remove(nbr)
    return neighbors


def check_body_overlap(neighboring_points: list, body_coords: list, wall_coords: list):
    """Counts how many of a point's neighbors are occupied by the snake's body."""
    return sum(1 for pt in neighboring_points if pt in body_coords or pt in wall_coords)



def get_movement_direction(prev, curr):
    x1, y1 = prev
    x2, y2 = curr

    if y2 == y1 and x2 == x1 - 1:
        return "left"
    elif y2 == y1 and x2 == x1 + 1:
        return "right"
    elif x2 == x1 and y2 == y1 - 1:
        return "straight"
    elif x2 == x1 and y2 == y1 + 1:
        return "straight"
def find_next_move(grid_height, grid_width, food, walls, score, my_snake_direction, my_snake_body, enemy_snakes):
    nbrs = find_neighbors(my_snake_body[0], my_snake_body, list(walls), my_snake_direction, grid_height, grid_width)
    fruit_coords = list(food)[0]
    move_scores = {}
    for move in nbrs:
        move_scores[move] = {
            'dist': manhattan_distance.manhattan_distance(move, fruit_coords),
            'overlap_factor': check_body_overlap(find_neighbors(move, my_snake_body, list(walls), my_snake_direction, grid_height, grid_width), my_snake_body, list(walls))
        }
    
    best_move =  min(move_scores, key=lambda k: (move_scores[k]['dist']))


    direction = get_movement_direction(my_snake_body[0], best_move)

    return direction 
    



    
    