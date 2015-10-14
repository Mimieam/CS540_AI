def distance_from_den (player, opponent):
    dist = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        distance = player[_animal].distance_from(opponent.den)
        if distance == 1:
            distance += 30
        if distance == 2:
            distance += 20
        if distance == 3:
            distance += 10
        print "[%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, opponent.den, player[_animal].distance_from(opponent.den))
        dist += distance
    return dist  # - because the smaller the distance the better for us

def remaining_pieces(player, opponent):
    animal_alive = 0
    for _animal in player:
        if not player[_animal].is_dead:
            animal_alive += 1
    return animal_alive

def can_capture(player, opponent):
    dist = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        for pray in [pray for pray in opponent if pray != 'den']:
            if not opponent[pray].is_dead:
                distance = player[_animal].distance_from(opponent[pray])
                if player[_animal] > opponent[pray] and distance == 1:
                    print "[%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, player[_animal].distance_from(opponent[pray]))
                    dist += 10
    return dist

def can_be_captured(player, opponent):
    dist = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        for pray in [pray for pray in opponent if pray != 'den']:
            if not opponent[pray].is_dead:
                distance = player[_animal].distance_from(opponent[pray])
                if player[_animal] < opponent[pray] and distance == 1:
                    print "can be can_be_captured [%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, distance)
                    dist -= 1
                #     return dist
                to_den = player[_animal].distance_from(opponent.den)
                if  player[_animal] < opponent[pray] and distance == 2 == to_den:
                    print "can_be_captured 2 away- [%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, distance)
                dist += 1
                # else:
                #     dist -= 10 * distance
    return dist

def in_danger(player, opponent, animal="tiger"):
    """
    check if a dangerous enemy is very close
    """
    dangerLevel = {
        'tiger': 5,
        'elephant': 5,
        'mouse': 2,
        'wolf': 2,
    }
    in_danger = 0
    if player[animal].is_dead:
        return in_danger
    for hostile in opponent:
        if not opponent[hostile].is_dead:
            if opponent[hostile] >  player[animal]:
                if player[animal].distance_from(opponent[hostile]) <=3:
                    in_danger += 1 * dangerLevel[animal]
                    print "[%s]%s is in DANGER from [%s]%s = %s" % ( player.name, animal, opponent.name, opponent[hostile], in_danger)

    return in_danger

# def hunted(player, opponent):
#     """
#      return a - value if i a piece can be captured indicating that this move is not good
#     """
#     res = 0
#     for animal in player:
#         if player[animal].is_dead:
#             continue
#         for hunter in opponent:
#             if not opponent[hunter].is_dead:
#                 if player[animal].distance_from(opponent[hunter]) <= 2:
#                     if player[animal] < opponent[hunter]:
#                         res -= 1
#                 print "[%s]%s is hunted by [%s]%s = %s" % ( player.name, animal, opponent.name, hunter, player[animal].distance_from(opponent[hunter]))
#     print hunted.__name__, res
#     return res

# def hunting_mode(player, opponent, animal='elephant'):
#     res = 0

#     if player[animal].is_dead:
#         return res
#     else:
#         for pray in opponent:
#             if not opponent[pray].is_dead:
#                 if player[animal].distance_from(opponent[pray]) <= 2:
#                     if player[animal] > opponent[pray]:
#                         print "[%s]%s hunting [%s]%s = %s" % ( player.name, animal, opponent.name, pray, player[animal].distance_from(opponent[pray]))
#                         res += 1

#                 # else:
#                 #     dist -= 3 * player[animal].distance_from(opponent[pray])
#     if animal == "elephant":
#         res += 5
#     print animal, " is done HUNTING ... res = ", res
#     print hunting_mode.__name__, res
#     return res

def distance_from_all_prays(player, opponent):
    dist = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        for pray in opponent:
            if not opponent[pray].is_dead:
                if player[_animal] > opponent[pray]:
                    print "[%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, player[_animal].distance_from(opponent[pray]))
                    dist += player[_animal].distance_from(opponent[pray])
    print __name__, dist
    return dist



def apply_to_both(board, players, fn):
    res = [0, 0]
    # sum the remaining piece for each player and returns the difference
    for idx, player in enumerate(players):
        if idx % 2 == 0:
            # print player
            opponent = players[1]
            res[0] = fn(player, opponent)
        else:
            # print player
            opponent = players[0]
            res[1] = fn(player, opponent)
    print fn.__name__, res[0] - res[1]
    return res[0] - res[1]

def apply_this_to_me_and_that_to_opponent(board, players, fn1, fn2, animal='elephant'):
    res = [0, 0]
    # sum the remaining piece for each player and returns the difference
    for idx, player in enumerate(players):
        if idx % 2 == 0:
            # print player
            opponent = players[1]
            res[0] = fn1(player, opponent, animal)
        else:
            # print player
            opponent = players[0]
            res[1] = fn2(player, opponent, animal)
    return res[0] - res[1]

# print apply_to_both("", ["234234","111"], remaining_pieces)

# print remaining_pieces("", ["234234","111"], lambda x: int(x))
