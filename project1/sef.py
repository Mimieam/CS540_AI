def remaining_pieces(player):
    animal_alive = 0
    for _animal in player:
        if not player[_animal].is_dead:
            animal_alive +=1
    return animal_alive

def apply_to_both(board, players, fn):
    res = [0,0]
    # sum the remaining piece for each player and returns the difference
    for idx, player in enumerate(players):
        if idx%2 == 0:
            print player
            res[0] = fn(player)
        else:
            print player
            res[1] = fn(player)
    return res[0] - res[1]

# print apply_to_both("", ["234234","111"], remaining_pieces)

# print remaining_pieces("", ["234234","111"], lambda x: int(x))
