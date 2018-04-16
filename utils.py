from constants import P2P_PIXELS, PIECE_RADIUS_PIXELS, BOARD_SIZE


def index_to_pixel(x):
    """Given a point index, return the corresponding pixel. The Index can be either row or column"""
    return P2P_PIXELS + P2P_PIXELS * x


def pixels_to_indices(pixel_x, pixel_y):
    """Given a point pixels, go through all points on the board to see which point is the intended selection. 

    :return: the selected point indices. If not found, return None"""
    # TODO: optimize this method

    square_distance_threshold = PIECE_RADIUS_PIXELS ** 2  # max distance allowed between the clicked position and the selected point
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            square_distance = (pixel_x - index_to_pixel(i)) ** 2 + (pixel_y - index_to_pixel(j)) ** 2
            if square_distance <= square_distance_threshold:
                return i, j
