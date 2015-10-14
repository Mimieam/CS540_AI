#    |1|2|3|4|5|6|7|8|
# 1|a| | | | | | | | |
# 2|b| | | | | | | | |
# 3|c| | | | | | | | |
# 4|d| | | | | | | | |
# 5|e| | | | | | | | |
# 6|f| | | | | | | | |
# 7|g| | | | | | | | |
# 8|h| | | | | | | | |
# 9|i| | | | | | | | |

import logging
import logging.handlers
import traceback
from helpMenu import parser

from helpers import *
from minimax import minimax, available_moves
from alphaBetaMinimax import alphaBetaMinimax, available_moves, count
from timeit import default_timer as timer

from sef import *


LOGGER = logging.getLogger("Animal_checker")
LOGGER.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler("./animal_checker2.log", mode='w')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# add the handlers to LOGGER
LOGGER.addHandler(ch)
# LOGGER.addHandler(fh)


INITIAL_LOCATIONS = {
    'player1':{
        'M': '6i',
        'E': '2i',
        'T': '5h',
        # 'T': '3c',
        'W': '3h',
        'DEN': '4i',
    },
    'player2': {
        'M': '2a',
        'E': '6a',
        'T': '3b',
        'W': '5b',
        'DEN': '4a',
    }
}


def get_user_input():
    """
        T down  -> Tiger move down
        M up  -> mouse move up
        E left -> go left
        W right -> wolf go right

    """
    while 1:
        animals_set = {
            "t": "tiger",
            "m": "mouse",
            "e": "elephant",
            "w": "wolf",
        }
        directions = {
            "u": "up",
            "d": "down",
            "l": "left",
            "r": "right",
        }
        try:
            LOGGER.debug("Your Turn Make a Move:  ( i.e. ~ T down ) ")
            _input = raw_input()
            # print _input.lower().strip().split(" ")[3:]
            _animal, _direction = _input.lower().strip().split(" ")[:2]

            LOGGER.debug("User Input: %s move %s" % (_animal, _direction))
            if _animal[0] in animals_set.keys() and _direction[0] in directions.keys():
                return animals_set[_animal[0]], directions[_direction[0]]
            elif _animal == "undo":
                return "undo", None
            else:
                # print _animal in animals_set.keys() and _direction in directions.keys()
                raise InvalidUserInputError
        except Exception, e:
            print traceback.format_exc(e)


class Animal(object):
    """docstring for Animal"""
    def __init__(self, _type, owner=None, verbose=False):
        self._type = _type
        self._capturable = ['den']
        self._verbose = verbose
        self.location = None
        self._row_col_location = None
        self.owner = owner
        self.is_dead = False
        self.neighbor=[]

    def __repr__(self):
        return ' %s ' % (self._type[0].upper() if self.owner.lower() == 'player1' else self._type[0].lower())

    def __lt__(self, other_animal):
        if hasattr(self, '_type'):

            return other_animal.can_capture(self)
        else:
            return True
        #     return other_animal.can_capture(str(self))

    def __gt__(self, other_animal):
        if hasattr(other_animal, '_type'):
            # print "other_animal", other_animal,  self._verbose
            return self.can_capture(other_animal)
        else:
            # print self.can_capture(other_animal)
            return True

    def get_initial_location(self):
        self.location = INITIAL_LOCATIONS[self.owner][self.get_symbol()]
        return self.location

    def can_move_to(self, new_location, new_row=None, new_col=None, _board=None):
        ''' returns (status, (new_row, new_col)) '''
        try:
            if self.is_dead:
                raise DeadAnimalException("\nDear %s, \n Sorry I'm dead.\n \t ~love your dead %s" % (self.owner, self._type))

            # print "new_location", new_location, new_row, new_col

            cur_row, cur_col = get_xy_coordinates(self.location)
            if not (new_row and new_col):
                # print "%s - %s" % (new_row, new_col)
                # print new_location
                new_row, new_col = get_xy_coordinates(new_location)
            #  left, up , right , down
            # print cur_row, cur_col
            # print new_row, new_col

            _neighbor = get_neighbor(cur_row, cur_col)
            self.neighbor = []
            [self.neighbor.append(item) for item in _neighbor.values() if item and self > _board[item[0] - 1][item[1] - 1]]
            # print _neighbor, self.neighbor
            # LOGGER.debug("Actual Available Moves = %s" % [get_alpha_numeric_coordinates(*x) +" -> "+str(x) for x in self.neighbor])
            # LOGGER.debug( "(%s)[%s] can move to %s ? = %s" % (self,self.owner,(new_row, new_col),(new_row, new_col) in self.neighbor))

            return ((new_row, new_col) in self.neighbor, (new_row, new_col))
        except Exception, e:
            # print str(traceback.format_exception_only(type(e), e)[0])
            print traceback.format_exc(str(e))
            return (False, (0, 0))

    def can_capture(self, other_animal):
        res = True if other_animal._type.lower() in self._capturable and \
                    other_animal.owner != self.owner else False
        verbose_status = ''
        if self._verbose:
            if res:
                verbose_status = 'The [%s](%s)' % (self._type, self.owner[0::1]) + \
                                 ' can capture this [%s](%s)' % (other_animal._type, other_animal.owner[0::1])
            else:
                verbose_status = 'The [%s](%s)' % (self._type, self.owner[0::1]) + \
                                 ' can NOT capture this [%s](%s)' % (other_animal._type, other_animal.owner[0::1])
            print verbose_status
        return res

    def _move(self, direction):
        ''' Syntatic Sugar function  to be able to move in any direction without entering the coordinates'''
        _nb =  get_neighbor(*get_xy_coordinates(self.location))
        print '[%s](%s) attempt to move to %s' % (self._type, self.owner, direction)
        if _nb[direction]:
            return get_alpha_numeric_coordinates(*_nb[direction])
        else:
            print '[%s](%s) can\'t move %s' % (self._type, self.owner, direction)
            raise OutOfBoardException("[%s](%s) Attempted to move outside the board..." % (self._type, self.owner))

    def is_captured(self):
        self.is_dead = True

    def get_symbol(self):
        return self._type[0].upper()

    def get_location(self):
        return self.location

    def distance_from(self, other_animal):
        if other_animal.is_dead:
            return DeadAnimalException(" [%s](%s) is trying to find the Ghost of this dead [%s](%s) ..." % (self._type, self.owner, other_animal._type, other_animal.owner))
        return abs(self._row_col_location[0] - \
                   other_animal._row_col_location[0]) + \
               abs(self._row_col_location[1] - \
                   other_animal._row_col_location[1])


class Den(Animal):
    """docstring for Den"""
    def __init__(self, owner=None, verbose=False):
        super(Den, self).__init__(self.__class__.__name__, owner=owner,
                                   verbose=verbose)
        self._capturable = []

    def __repr__(self):
        return '%s' % ('DEN' if self.owner.lower() == 'player1' else 'den')

    def is_captured(self):
        print  "Den Captured"
        self.is_dead = True


class Wolf(Animal):
    """docstring for Wolf"""
    def __init__(self, owner=None, verbose=False):
        super(Wolf, self).__init__(self.__class__.__name__, owner=owner,
                                   verbose=verbose)
        self._capturable += ['mouse', 'wolf']


class Mouse(Animal):
    """docstring for Mouse"""
    def __init__(self, owner=None, verbose=False):
        super(Mouse, self).__init__(self.__class__.__name__, owner=owner,
                                    verbose=verbose)
        self._capturable += ['mouse', 'elephant']


class Tiger(Animal):
    """docstring for Tiger"""
    def __init__(self, owner=None, verbose=False):
        super(Tiger, self).__init__(self.__class__.__name__, owner=owner,
                                    verbose=verbose)
        self._capturable += ['mouse', 'tiger', 'wolf']


class Elephant(Animal):
    """docstring for Elephant"""
    def __init__(self, owner=None, verbose=False):
        super(Elephant, self).__init__(self.__class__.__name__, owner=owner,
                                       verbose=verbose)
        self._capturable += ['tiger', 'wolf', 'elephant']


class Player(object):
    """docstring for Player"""
    def __init__(self, name='player1', location=None, verbose=False):
        self.name = name
        self.tiger = Tiger(verbose=verbose, owner=self.name)
        self.wolf = Wolf(verbose=verbose, owner=self.name)
        self.mouse = Mouse(verbose=verbose, owner=self.name)
        self.elephant = Elephant(verbose=verbose, owner=self.name)
        self.den = Den(verbose=verbose, owner=self.name)

    def __getitem__(self, key):
        """ return a animal by the key Name

        """
        return self.__dict__[key]

    def __iter__(self):
        return iter([item for item in self.__dict__ if item not in ['name', 'den']])


class AnimalChecker(object):
    """docstring for AnimalChecker"""
    def __init__(self, rows, cols, starting_player=1):
        self.rows = rows
        self.cols = cols
        self._board = []
        self._y_arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self.players = []
        self.setup()
        self.plys = 0
        self.starting_player = starting_player if starting_player in [1,2] else 1
        self.is_gameover = False
        self.last_move = move_tracker(self)

    def setup(self):

        self._board = self.build_board()
        self.players = self.init_players()
        for _player in self.players:
            self._move_animal(_player.tiger,
                              _player.tiger.get_initial_location())
            self._move_animal(_player.mouse,
                              _player.mouse.get_initial_location())
            self._move_animal(_player.wolf,
                              _player.wolf.get_initial_location())
            self._move_animal(_player.elephant,
                              _player.elephant.get_initial_location())

            self._set_den(_player)

    def init_players(self):
        Player1 = Player('player1', verbose=False)
        Player2 = Player('player2', verbose=False)
        return [Player1, Player2]

    def _set_den(self, player):
        # get den location for this player
        player.den.location = INITIAL_LOCATIONS[player.name]['DEN']  # change location
        player.den._row_col_location = get_xy_coordinates(player.den.location)
        # self._add_to_board(*get_xy_coordinates(player.den.location),
                               # content=player.den)  # remote  animal from previous location on board

    def _find_whose_turn(self):
        # print (self.plys + self.starting_player - 1) % 2
        return self.players[(self.plys + self.starting_player - 1) % 2 ].name

    def get_players(self):
        return self.players

    def get_current_game_state(self):
        return self

    def build_board(self):
        _board = []
        for row in xrange(0, self.rows):
            _board.append([])
            for col in xrange(0, self.cols):
                _board[row].append('   ')
        return _board

    def display_board(self, _board=[], raw=False, no_print=False):
        if not _board:
            _board = self._board
        current_player = self._find_whose_turn()
        board_str = ""
        if not raw:
            board_str = "\n[==============( %s Turn - total ply = %s )==============]\n\n" % (current_player, self.plys)
        for row_index in xrange(0, len(_board)):
            row = _board[row_index]

            curren_col = ''
            if not raw:
                if(row_index == 0):  # just to display the first header line
                    curren_col += '   |'
                    for col_index in xrange(0, len(_board[row_index])):
                        curren_col += ' ' + str(col_index + 1) + ' |'
                    curren_col += '\n'

                curren_col += '' + self._y_arr[row_index] + "->|"
            else:
                curren_col = '|'

            # print Den
            # make a den accessible to own animals
            for index, col in enumerate(row):
                if (row_index + 1, index + 1) == get_xy_coordinates(INITIAL_LOCATIONS['player1']["DEN"]):
                    if isinstance(col, Animal):
                        curren_col += '*' + str(col).strip() + '*|'
                    else:
                        curren_col += 'DEN|'
                elif (row_index + 1, index +1) == get_xy_coordinates(INITIAL_LOCATIONS['player2']["DEN"]):
                    if isinstance(col, Animal):
                        curren_col += '*' + str(col).strip() + '*|'
                    else:
                        curren_col += 'den|'
                else:
                    curren_col += '' + str(col) + '|'
            board_str += '%s\n' % curren_col
        if not raw:
            board_str += "\n[==================================================]\n"
        # LOGGER.info(board_str)
        if not no_print:
            print board_str
        return board_str

    def get_item_at(self, row, col):
        return self._board[row - 1][col - 1]

    def _add_to_board(self, row, col, content):
        try:
            # print "adding to board {%s,%s} = %s(%s)" % (row, col, content, content.owner)
            self._board[row - 1][col - 1] = content

        except IndexError:
            raise InvalidMoveException


    def _check_winner_state(self):
        currently_on_tile = self._board[0][3]
        if isinstance(currently_on_tile, Animal):  # check one of the player in on the wining tile
            if currently_on_tile.owner == 'player1':
                print "WE HAVE A WINNER !!", currently_on_tile.owner.upper(), "WON !!"
                self.is_gameover = True
                return True
        currently_on_tile = self._board[8][3]
        if isinstance(currently_on_tile, Animal):  # check one of the player in on the wining tile
            if currently_on_tile.owner == 'player2':
                print "WE HAVE A WINNER !!", currently_on_tile.owner.upper(), "WON !!"
                self.is_gameover = True
                return True

        for player in self.players:
            opponent = [p for p in self.players if player != p]
            if all(player[animal].is_dead == True for animal in player):
                print "WE HAVE A WINNER !!", opponent[0].name.upper(), "WON !!"
                return True


        return False

    def _move_animal(self, animal, where):
        ''' each animal keep track of it's last position '''
        try:

            self._add_to_board(*get_xy_coordinates(animal.location),
                               content='   ')  # remote  animal from previous location on board
            animal.location = where  # change location
            animal._row_col_location = get_xy_coordinates(where)  # change location
            self._add_to_board(*get_xy_coordinates(where),
                               content=animal)  # add animal to new location
        except Exception, e:
            print traceback.format_exc()
            raise e

    def move(self, animal, direction):
        '''Syntactic sugar to conveniently use directions instead of coordinates'''
        try:
            if animal.owner is self._find_whose_turn():
                new_location = animal._move(direction)
                if new_location:
                    return self._move(animal, new_location)
            # else:
            #     LOGGER.warning("Waiting on %s to play ..." % self._find_whose_turn())
        except OutOfBoardException, e:
            print traceback.format_exc(e)

    def ai_move(self, who, new_row=None, new_col=None, sef=0, player=None):
        return self._move(player[who], None, new_row, new_col)

    def _move(self, who, new_location=None, new_row=None, new_col=None):
        try:
            if self.is_gameover == True:
                print ("Game Over")
                return True

            if not new_location:
                # print who, new_location, new_row, new_col
                new_location = get_alpha_numeric_coordinates(new_row, new_col)

            cur_player = self._find_whose_turn()
            if who.owner is not cur_player:
                print "Waiting on %s to play ..." % cur_player
                # self.display_board()
                return False
            old_location = who.location
            status, (row, col) = who.can_move_to(new_location, new_row, new_col, self._board)
            # print status
            if not status:
                print "[%s](%s) can't move to %s" % (who._type, who.owner, new_location)
                self.display_board()
                return False
            # print who, ">", self.get_item_at(row, col)
            animal_on_tile = self.get_item_at(row, col)
            if isinstance(animal_on_tile, Animal):  # tile not empty
                res = who > animal_on_tile
                # print res, who.owner is not animal_on_tile.owner, who.owner, animal_on_tile.owner
                if (res and (who.owner is not animal_on_tile.owner)):
                    print 'BOOYA! [%s](%s) Captured [%s](%s)' % (who._type, who.owner, animal_on_tile._type, animal_on_tile.owner)
                    animal_on_tile.is_captured()
                    # self._move_animal(who, new_location)
                    if new_location:
                        self._move_animal(who, new_location)
                    else:
                        self._move_animal(who,  get_alpha_numeric_coordinates(new_row, new_col))

                else:
                    if isinstance(animal_on_tile, Den):
                        # print "tring to go in the den"
                        # self._move_animal(who, new_location)
                        if new_location:
                            self._move_animal(who, new_location)
                        else:
                            self._move_animal(who,  get_alpha_numeric_coordinates(new_row, new_col))

                    else:
                        print "can't do this - %s , %s" % (res, who.owner is not animal_on_tile.owner)
                        return False
            else:  # tile was empty ... just move up there if you can
                if new_location:
                    self._move_animal(who, new_location)
                else:
                    self._move_animal(who,  get_alpha_numeric_coordinates(new_row, new_col))


            self.plys +=1
            self.last_move.update(who, old_location, new_location, animal_on_tile)
            # self.display_board()
            # check Winning state
            # self._check_winner_state(who, new_location);
            return True
        except Exception, e:
            print traceback.format_exc(e)
            self.display_board()
            return False
            # raise e

    def undo(self):
        ''' undo a move using the move_tracker plugin '''
        # l_move = self.last_move
        self.last_move.revert()
        # LOGGER.warning(l_move)
        if self.is_gameover == True:
            self.is_gameover = False

if __name__ == '__main__':
    import sys
    print """
       | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    a->|   |   | m |*e*| w |   |   |
    b->|   |   |   | t |   |   |   |
    c->|   |   |   |   |   |   |   |
    d->|   |   |   |   |   |   |   |
    e->|   |   |   |   |   |   |   |
    f->|   |   |   |   |   |   |   |
    g->|   | E |   |   | T |   |   |
    h->|   |   | W |   |   |   |   |
    i->|   |   |   |DEN|   | M |   |
    """
    opening_book = {
        "offense": [
            ('mouse', 'down'),
            ('elephant', 'down'),
            ('elephant', 'down'),
            ('wolf', 'right'),
            ('elephant', 'left'),
            ('tiger', 'down'),
            ('mouse', 'down'),
            ('elephant', 'left'),
            ('wolf', 'down'),
            ('mouse', 'down'),
        ],
        "defense": [
            # ('elephant', 'down'),
            # ('elephant', 'down'),
            # ('elephant', 'left'),
            # ('elephant', 'left'),
            # ('mouse', 'down'),
            # ('tiger', 'right'),
            # ('elephant', 'left'),
            # ('tiger', 'down'),
            # ('wolf', 'down'),
            # ('mouse', 'down'),
        ],
    }

    try:
        print tigerAscii

        if len(sys.argv) < 3:
            parser.print_help()
            sys.exit()

        args = parser.parse_args()
        startingP = int(args.FirstPlayer[0])
        game = AnimalChecker(rows=9, cols=7, starting_player=startingP)
        game.setup()
        p1, p2 = game.get_players()

        player = {
            "1": p1,
            "2": p2,
        }
        _next=0
        while True:

            game.display_board()
            print "PLAYER Turn = ", game._find_whose_turn()
            if game._find_whose_turn() == 'player1':
                ani, loc = get_user_input()
                if ani=="undo":
                    game.undo()
                    continue
                status = game.move(p1[ani], loc)
                while not status:
                    ani, loc = get_user_input()
                    status = game.move(p1[ani], loc)

                game._check_winner_state();
                if game.is_gameover:
                    break;
            else:

                if game.plys < 10 :
                    ani, direction = opening_book['offense'][(_next)%len(opening_book['offense'])]
                    while not game.move(p2[ani], direction):
                        _next+=1
                        ani, direction = opening_book['offense'][(_next)%len(opening_book['offense'])]
                    _next+=1

                else:

                    start = timer()
                    # _, bestMove = minimax(game, 0, 4, p2, None)
                    _, bestMove = alphaBetaMinimax(game, -1000, 1000, 0, 4, p2, None)  # 2 or 4 ( not 3) for depth
                    end = timer()
                    # print bestMove
                    # bestMove = (p2[bestMove[0]], None,)+bestMove[1:-1]
                    # print bestMove
                    game.ai_move(player=p2, *bestMove)
                    # print game._move(*bestMove)
                    print " Total time %s" % (end - start)
                    alphaBetaMinimax.count = 0
                game._check_winner_state()
                if game.is_gameover:
                    break;

        game.display_board()

    except InvalidMoveException:
        print "Invalid Move, please try again"

