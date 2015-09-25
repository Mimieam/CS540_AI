def get_xy_coordinates(xy):
    if isinstance(xy, tuple):
        return xy
    x = None
    # print xy
    try:
        if 1 <= int(xy[0]) < 8:
            x = xy[0]
        else:
            raise IndexError
        y = xy[1]
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        return (int(x), arr.index(y) + 1)
    except (ValueError, IndexError, TypeError, KeyError):
        raise Exception("Could not convert input (%s) to {row, col} coordinates" % str(xy))


def in_board(row, col):
    in_row = (1 <= int(col) < 8)
    in_col = (1 <= int(row) < 10)
    res = in_row and in_col
    # print "in row (1 <= (row:%s) < 8) = %s , (1 <= (col:%s) < 10) = %s  " %
    # (row, in_row, col, in_col)
    return res


def get_actual_neighbor(cur_row=0, cur_col=0, str_loc=None):
    if str_loc:
        cur_row, cur_col = get_xy_coordinates(str_loc)[::-1]
    _neighbor = {
        'left': (cur_row, cur_col - 1) if in_board(cur_row, cur_col - 1) else None,
        'up': (cur_row - 1, cur_col) if in_board(cur_row - 1, cur_col) else None,
        'right': (cur_row, cur_col + 1) if in_board(cur_row, cur_col + 1) else None,
        'down': (cur_row + 1, cur_col) if in_board(cur_row + 1, cur_col) else None
    }
    neighbor = []
    [neighbor.append(item) for item in _neighbor.values() if item]
    return neighbor



def node(state_str="", children=[]):
    '''An Node state_str is the current_state (the position of all the player in the board as a string

    '''
    return {"state": state_str, "children": children}
