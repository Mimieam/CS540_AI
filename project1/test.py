from AnimalChecker import *
try:
    # T = Tiger(verbose=True, owner=Player('testPlayer').name)
    # E = Elephant(verbose=True, owner=Player('testPlayer').name)
    # W = Wolf(verbose=True, owner=Player('testPlayer').name)
    # M = Mouse(verbose=True, owner=Player('testPlayer').name)
    # D = Den(verbose=True, owner=Player('testPlayer2').name)

    # Player1 = Player('player1')
    # Player2 = Player('player2')

    # print Player1.tiger
    # print Player1.wolf
    # # print T.can_capture('elephant')
    # # print T.can_capture('WOLF')
    # print E._capturable
    # print E > D
    # print W > D
    # print T > D
    # print M > D
    # print T > E
    # print E > T, E > M

    # print T.get_symbol()
    # print M.get_symbol()

    # # print '%s' % T
    game = AnimalChecker(rows=9, cols=7)
    # game.setup()
    p1, p2 = game.get_players()
    print game.display_board()
    # game._move(p1.tiger, "6h")
    # game._move(p2.wolf, "6b")
    game._move(p1.mouse, "5i")  # ai moves
    game.move(p1.mouse, "up")  # human moves
    game.move(p2.mouse, "down")
    game.move(p1.mouse, "up")
    game.move(p2.mouse, "down")
    game.move(p1.mouse, "up")
    game.move(p2.mouse, "down")
    game.move(p2.tiger, "down")
    game.move(p1.mouse, "up")
    game.move(p2.mouse, "down")
    # print p2.wolf._move("left")
    # print p2.wolf._move("up")
    # print p2.wolf._move("right")
    # print p2.wolf._move("down")
    # game.move(p2.wolf, "6d")
    # game.move(p1.wolf, "6e")
    # game.move(p2.wolf, "6f")
    # game.move(p1.wolf, "6g")
    # game.move(p1.tiger, "6g")
    # game.move(p2.wolf, "7g")
    # print game.display_board()
    # game.move(Player1.tiger, '4g')
    # # print game.move(Player1.wolf, '3g')
    # # game.move(Player1.mouse, '7b')
    # game.move(Player2.mouse, '5b')
    # game.move(Player1.mouse, '5i')
    # print Player1.mouse.location
    # print Player1.mouse.can_move_to('7b')
    # print Player1.mouse.can_move_to('5c')

    # # game.move(Player2.mouse, '3b')
    # # game.move(Player2.elephant, '4b')
    # print Player1.mouse.location

    # # print game.move(Player1.tiger, '3b')
    # # print game.move('T', '3g')
    # # print game.move('M', '4g')
    # # # print game.add_to_board(*get_xy_coordinates('2a')[::-1], content="T")
    # print game.display_board()

    # print get_xy_coordinates('2a')
    # print get_xy_coordinates('2a')[::-1]
    # print get_alpha_numeric_coordinates(2, 1)
    # print get_alpha_numeric_coordinates(*get_xy_coordinates('2a'))
    # print get_xy_coordinates(get_alpha_numeric_coordinates(5, 3))
except InvalidMoveException:
    print "Invalid Move, please try again"
