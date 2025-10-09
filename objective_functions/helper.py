from objective_functions import manhattan_distance, queue_class
from global_tracker.best_path import NODE_QUEUE
import heapq 
def find_neighbors(head_coords, body_coords, walls_coords, grid_height, grid_width, enemy_snakes):
   
    
    x, y = head_coords
    potential_neighbors = [
        (x - 1, y) if x - 1 >= 0 else None,      # Left
        (x + 1, y) if x + 1 < grid_width else None, # Right
        (x, y + 1) if y + 1 < grid_height else None, # Up
        (x, y - 1) if y - 1 >= 0 else None      # Down
    ]
    
    # Use a list comprehension for a safe and clean filter
    long_snake_list = []
    for snake in enemy_snakes:
        
        long_snake_list.extend(snake)

    long_snake_list = list(set(long_snake_list))
    valid_neighbors = [
        n for n in potential_neighbors 
        if n is not None and (n not in body_coords and n not in walls_coords and n not in long_snake_list )
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
    


# def breadth_first_search(head_coords: tuple, fruit_coords: tuple,  body_coords: list, wall_coords: list, enemy_snakes: list, grid_height: int, grid_width : int):
#     # NODE_QUEUE
#     NODE_QUEUE.dequeue_node()
    
#     neighbors = find_neighbors(head_coords=head_coords, body_coords=body_coords, walls_coords= wall_coords,
#                                grid_height= grid_height, grid_width=grid_width, enemy_snakes= enemy_snakes)

#     print(f'These are the neighbors')
#     print(neighbors)
    
#     new_neighbors = [nbr for nbr in neighbors if nbr not in NODE_QUEUE.visited_nodes]
    
#     print(f'NEW NEIGHBORS : {new_neighbors}')
#     mdist_list = np.array([manhattan_distance.manhattan_distance(nbr, fruit_coords) for nbr in new_neighbors])

#     print(f'DISTANCE LIST : {mdist_list}')
#     min_index = np.argmin(mdist_list)
#     best_node = new_neighbors[min_index]

#     print(f'BEST NODE : {best_node}')

#     NODE_QUEUE.enqueue(best_node)
    
#     print(f' VISITED NODES : {NODE_QUEUE.visited_nodes}')
#     if best_node == fruit_coords:
#         NODE_QUEUE.visited_nodes = []
#     else:
#         NODE_QUEUE.visited_nodes.append(best_node)
#     return best_node
    

    # #     node_queue.enqueue(nbr)
    # # next_node = node_queue.dequeue_node()

    # path = []

    # # while next_node != fruit_coords:
    # #     path.append(next_node)        
    # #     neighbors = find_neighbors(head_coords = next_node, body_coords=body_coords, walls_coords= wall_coords,
    # #                            grid_height= grid_height, grid_width=grid_width, enemy_snakes= enemy_snakes)
        
        
    # #     mdist_list = [manhattan_distance.manhattan_distance(nbr, fruit_coords) for nbr in neighbors]
        
    # #     zipped_nbr_dist_list = zip(mdist_list, neighbors)

    # #     sorted_pairs  = sorted(zipped_nbr_dist_list)
    # #     sorted_neighbors = [neighbor for distance, neighbor in sorted_pairs]


    # #     for nbr in sorted_neighbors:
    # #         node_queue.enqueue(nbr)
    # #     next_node = node_queue.dequeue_node()

    # # print('BFS Ended')
    # # return path 
    

def a_star_search(head_coords: tuple, fruit_coords: tuple, body_coords: list, wall_coords: list, enemy_snakes: list, grid_height: int, grid_width: int):
  
    all_obstacles = set(body_coords) | set(wall_coords)
    for snake in enemy_snakes:
        all_obstacles.update(snake)


    open_set = [(0, head_coords)]
    heapq.heapify(open_set)

    came_from = {}
    
    g_score = { (x, y): float('inf') for x in range(grid_width) for y in range(grid_height) }
    g_score[head_coords] = 0

    f_score = { (x, y): float('inf') for x in range(grid_width) for y in range(grid_height) }
    f_score[head_coords] = manhattan_distance.manhattan_distance(head_coords, fruit_coords)
    
    visited = set()

    while open_set:
        _, current_coords = heapq.heappop(open_set)

        if current_coords == fruit_coords:
            path = []
            while current_coords in came_from:
                path.append(current_coords)
                current_coords = came_from[current_coords]
            path.append(head_coords)
            return path[::-1]

        visited.add(current_coords)

        neighbors = find_neighbors(current_coords, body_coords, wall_coords, grid_height, grid_width, enemy_snakes)
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            tentative_g_score = g_score[current_coords] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_coords
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score -  manhattan_distance.manhattan_distance(neighbor, fruit_coords)
                
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []
        
    
        
def check_body_overlap(neighboring_points: list, body_coords: list, wall_coords: list, enemy_snakes: list):
    """Counts how many of a point's neighbors are occupied by the snake's body."""
    overlap = 0

    for  pt in neighboring_points:
        for bd_point in body_coords:
            overlap = manhattan_distance.manhattan_distance(bd_point, pt)
        for bd_point in wall_coords:
            overlap = manhattan_distance.manhattan_distance(bd_point, pt)
        for enemy_snake in enemy_snakes:
            overlap = manhattan_distance.manhattan_distance(bd_point, enemy_snake[0])

    
    if len(neighboring_points) == 0:
        return 0
    return overlap / (len(neighboring_points) + len(wall_coords) + len(enemy_snakes))

    


def find_best_fruit(head_coords: tuple, fruit_coords_list: list):
    least_length = manhattan_distance.manhattan_distance(head_coords=head_coords, fruit_coords=fruit_coords_list[0])
    best_fruit = fruit_coords_list[0]

    for coords in fruit_coords_list:
        new_length = manhattan_distance.manhattan_distance(head_coords = head_coords, fruit_coords=coords)
        if new_length < least_length:
            least_length = new_length 
            best_fruit = coords 
    
    return best_fruit 



def find_next_move(grid_height, grid_width, food, walls, score, my_snake_direction, my_snake_body, enemy_snakes):
    # try:
    best_fruit = find_best_fruit(my_snake_body[0], list(food))
    head = my_snake_body[0]
    
    path = a_star_search(head, best_fruit, my_snake_body, 
                         list(walls), enemy_snakes, grid_height, grid_width)
    if path and len(path) > 1:
        return path[1]
    else:
  
        neighbors = find_neighbors(head, my_snake_body, list(walls), grid_height, grid_width, enemy_snakes)
        if neighbors:
            min_overlap = 100
            best_nbr = neighbors[0]
            for nbr in neighbors:
                internal_neighbors = find_neighbors(head, my_snake_body, walls, grid_height, grid_width, enemy_snakes)
                overlap_score = check_body_overlap(internal_neighbors, my_snake_body, walls, enemy_snakes)
                if overlap_score< min_overlap:
                    best_nbr = nbr 
            return best_nbr 
        else:
            if my_snake_direction == 'UP':
                return (head[0], head[1] + 1)
            elif my_snake_direction == 'DOWN':
                return (head[0], head[1] - 1)
            elif my_snake_direction == 'LEFT':
                return (head[0] - 1, head[1])
            else: 
                return (head[0] + 1, head[1])




    



    
