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
from helpers import move_tracker

LOGGER = logging.getLogger("Animal_checker")
LOGGER.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("animal_checker2.log", mode='w')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to LOGGER
LOGGER.addHandler(ch)
LOGGER.addHandler(fh)


INITIAL_LOCATIONS = {
    'player1':{
        'M': '6i',
        'E': '2i',
        # 'T': '5h',
        'T': '3c',
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


class InvalidMoveException(Exception):
    pass


class OutOfBoardException(Exception):
    pass


class DeadAnimalException(Exception):
    pass


# HELPERS
def get_xy_coordinates(xy):
    x = None
    if isinstance(xy, tuple):
        return xy
    try:
        if 1 <= int(xy[0]) < 8:
            x = xy[0]
        else:
            raise IndexError
        y = xy[1]
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        return (arr.index(y) + 1, int(x))
    except (ValueError, IndexError, TypeError, KeyError):
        raise InvalidMoveException("Could not convert input (%s) to {row, col} coordinates" % str(xy))


def get_alpha_numeric_coordinates(y, x):
    try:
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        if not (1 <= int(x) < 8):
            raise IndexError
        return '%s%s' % (int(x), arr[int(y) - 1])
    except (ValueError, IndexError, TypeError):
        raise InvalidMoveException("Could not convert back {%s, %s} - Out of board range" % (y, x))


def in_board(row, col):
    in_row = (1 <= int(col) < 8)
    in_col = (1 <= int(row) < 10)
    res = in_row and in_col
    # print "in row (1 <= (row:%s) < 8) = %s , (1 <= (col:%s) < 10) = %s\
    #   " % (row, in_row, col, in_col)
    return res


def get_neighbor(cur_row, cur_col):
    return {
        'left': (cur_row, cur_col-1) if in_board(cur_row, cur_col-1) else None,
        'up': (cur_row-1, cur_col) if in_board(cur_row-1, cur_col) else None,
        'down': (cur_row+1, cur_col) if in_board(cur_row+1, cur_col) else None,
        'right': (cur_row, cur_col+1) if in_board(cur_row, cur_col+1) else None
    }


def AI_getBestMove(current_game_state):
    return sef(current_game_state)


def get_user_input_and_make_move():
    """
        T down  -> Tiger move down
        M Up  -> mouse move up
        E left -> go left
        W right -> wolf go right

    """
    try:
        _input = raw_input()
        _animal, _direction = _input.split(" ")

        LOGGER.debug("User Input: %s move %s" % (_animal, _direction))
    except Exception, e:
        raise e


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

    def can_move_to(self, new_location, new_row=None, new_col=None):
        ''' returns (status, (new_row, new_col)) '''
        try:
            if self.is_dead:
                raise DeadAnimalException("\nDear %s, \n Sorry I'm dead.\n \t ~love your dead %s" % (self.owner, self._type))

            print "new_location", new_location, new_row, new_col

            cur_row, cur_col = get_xy_coordinates(self.location)
            if not (new_row and new_col):
                # print "%s - %s" % (new_row, new_col)
                print new_location
                new_row, new_col = get_xy_coordinates(new_location)
            #  left, up , right , down
            # print cur_row, cur_col
            # print new_row, new_col

            _neighbor = get_neighbor(cur_row, cur_col)
            self.neighbor = []
            [self.neighbor.append(item) for item in _neighbor.values() if item]
            print _neighbor, self.neighbor
            print "(new_row, new_col) in self.neighbor", (new_row, new_col) in self.neighbor
            print [get_alpha_numeric_coordinates(*x) for x in self.neighbor]
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
        #     return (res, verbose_status)
        # else:
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
    def __init__(self, name='player1', location=None):
        self.name = name
        self.tiger = Tiger(verbose=True, owner=self.name)
        self.wolf = Wolf(verbose=True, owner=self.name)
        self.mouse = Mouse(verbose=True, owner=self.name)
        self.elephant = Elephant(verbose=True, owner=self.name)
        self.den = Den(verbose=True, owner=self.name)

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
        Player1 = Player('player1')
        Player2 = Player('player2')
        return [Player1, Player2]

    def _set_den(self, player):
        # get den location for this player
        player.den.location = INITIAL_LOCATIONS[player.name]['DEN']  # change location
        player.den._row_col_location = get_xy_coordinates(player.den.location)
        # self._add_to_board(*get_xy_coordinates(player.den.location),
                               # content=player.den)  # remote  animal from previous location on board

    def _find_whose_turn(self):
        print (self.plys + self.starting_player - 1) % 2
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

    def display_board(self, _board=[], raw=False):
        if not _board:
            _board = self._board
        current_player = self._find_whose_turn()
        board_str = "\n[==============( %s Turn - total moves = %s )==============]\n\n" % (current_player, self.plys)
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

        board_str += "\n[======================================]\n"
        LOGGER.info(board_str)
        return board_str

    def get_item_at(self, row, col):
        return self._board[row - 1][col - 1]

    def _add_to_board(self, row, col, content):
        try:
            # print "adding to board {%s,%s} = %s(%s)" % (row, col, content, content.owner)
            self._board[row - 1][col - 1] = content

        except IndexError:
            raise InvalidMoveException

    def _check_winner_state(self, hunter, pray):
        if isinstance(pray, Den):
            print "WE HAVE A WINNER !!", hunter.owner.upper(), "WON !!"
            self.is_gameover = True

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
            print str(e)

    def _move(self, who, new_location=None, new_row=None, new_col=None):
        try:
            if self.is_gameover:
                print ("Game Over")
                return True

            if not new_location:
                print who, new_location, new_row, new_col
                new_location = get_alpha_numeric_coordinates(new_row, new_col)

            cur_player = self._find_whose_turn()
            if who.owner is not cur_player:
                LOGGER.warning("Waiting on %s to play ..." % cur_player)
                self.display_board()
                return False
            old_location = who.location
            status, (row, col) = who.can_move_to(new_location, new_row, new_col)
            print status
            if not status:
                print ("[%s](%s) can't move to %s" % (who._type, who.owner, new_location))
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
                        print "tring to go in the den"
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
            self.display_board()
            # check Winning state
            self._check_winner_state(who, animal_on_tile);
            return True
        except Exception, e:
            print traceback.format_exc(e)
            self.display_board()
            return False
            # raise e

    def undo(self):
        ''' undo a move using the move_tracker plugin '''
        print self.last_move
        self.last_move.revert()

if __name__ == '__main__':

    try:
        game = AnimalChecker(rows=9, cols=7, starting_player=1)
        # game.setup()
        p1, p2 = game.get_players()
        game.display_board()
        # game._move(p1.tiger, "6h")
        # game._move(p2.wolf, "6b")
        # game simulation
        # # get_user_input_and_make_move()
        # for step in xrange(0,30):
        #     LOGGER.debug(id(game.get_current_game_state()))
        #     animal2, location2 = AI_getBestMove(game.get_current_game_state())
        #     while not game.move(p2[animal2], location2):
        #         animal2, location2 = AI_getBestMove(game.get_current_game_state())
        #     LOGGER.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++CUrrent step COUNT = %s " % step)
        #     # game.move(p2["mouse"],"down")
        #     # animals[random.randint(0, 3)]
        #     animal, location = AI_getBestMove(game.get_current_game_state())
        #     while not game.move(p1[animal], location):
        #         animal, location = AI_getBestMove(game.get_current_game_state())

        #     # game.ai move


        # game._move(p2.mouse, "5i")  # ai moves
        game.move(p2.mouse, "right")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.mouse, "right")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.mouse, "right")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.elephant, "left")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.elephant, "left")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.elephant, "down")
        game.move(p1.mouse, "left")  # human moves
        game.move(p2.elephant, "left")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "up")
        # game.move(p2.mouse, "down")
        # game.move(p1.tiger, "right")
        # game.move(p2.mouse, "up")
        # game.move(p1.tiger, "right")
        # game.move(p2.mouse, "right")
        # game.move(p1.mouse, "up")
        # game.move(p2.mouse, "up")

    except InvalidMoveException:
        print "Invalid Move, please try again"
