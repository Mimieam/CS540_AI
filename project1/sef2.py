# sef2.py

def remaining_pieces(player, opponent):
    animal_alive = 0
    for _animal in player:
        if not player[_animal].is_dead:
            animal_alive += 1
    return animal_alive
# piece importance
def piece_importance(player, opponent, _animal):
    res = 0
    if player[_animal].is_dead:
        return -10
    #distance from enemie DEN
    dist = -player[_animal].distance_from(opponent.den)

    #remaining piece
    # 0 = balanced
    # 0 < opponent advantage
    # 0 > current player advantage
    rem = remaining_pieces(player, opponent) - remaining_pieces(opponent, player)

    #can be captured ( = -1 piece)
    is_safe = 0
    for pray in [pray for pray in opponent if pray != 'den']:
        if not opponent[pray].is_dead:
            distance = player[_animal].distance_from(opponent[pray])
            if player[_animal] < opponent[pray] and distance == 1:
                print "can be can_be_captured [%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, distance)
                is_safe -= 1
            #     return dist
            to_den = player[_animal].distance_from(opponent.den)
            if  player[_animal] < opponent[pray] and distance == 2 == to_den:
                print "can_be_captured 2 away- [%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, distance)
                is_safe += 1
    print _animal, "IMPORTANCE : "
    print "\tdistance_from_den = %s" % dist
    print "\tremaining_pieces = %s " % rem
    # print "\tcan_capture = %s" % cap
    print "\tcan_be_capture = %s" % is_safe

    return dist + is_safe + 2 *rem
