from AnimalChecker import *
from sef import _sef, StageEvaluationBoard


if __name__ == '__main__':
    game = AnimalChecker(rows=9, cols=7, starting_player=1)
    game.setup()
    p1, p2 = game.get_players()


    stage_board = StageEvaluationBoard(game, game._board)
    stage_board.generate_children_nodes(p1)
    stage_board.minimax(stage_board.get_root_node(p1),1, 3, p1)
    # stage_board.available_moves(p1)
    # print stage_board.get_board_state(game)["player1"]
    # print stage_board.minimax(stage_board.get_board_state(game)['player1'], 0, 3)
    # print stage_board.available_moves(p1)
    # print stage_board.available_moves(p2)

    # root_node = node("", stage_board.available_moves(p1, str_coordinate=True))
    # tree = {
    #     'children': []
    # }
    # print "root_node", root_node
    # # for player in game.players
    # node = stage_board.available_moves(p1, str_coordinate=True)
    # for item in node:
    #     print node[item]
    #     for new_location in node[item]:
    #         # print'[%s]%s' % (item, new_location)
    #         # print game.players[0][item], new_location
    #         # print in_board(*new_location)
    #         game._move(game.players[0][item], new_location, new_row=new_location[0], new_col=new_location[1])
    #         tree["children"] += [stage_board.get_board_state(game)]
    #         game.undo()
    #         # game.display_board()
    #         # return ""
    # # print stage_board.get_board_state(game)
    # for item in  enumerate(tree['children']):
    #     print item
    #             # make_move


