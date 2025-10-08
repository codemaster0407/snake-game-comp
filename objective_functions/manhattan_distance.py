def manhattan_distance(head_coords : tuple, fruit_coords: tuple):

    manh_distance = abs(head_coords[0] - fruit_coords[0]) + abs(fruit_coords[1] - head_coords[1])
    return manh_distance 