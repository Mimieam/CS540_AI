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

logger = logging.getLogger("Animal_checker")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("animal_checker.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


INITIAL_LOCATIONS = {
    'player1':{
        'M': '6i',
        'E': '2i',
        'T': '5h',
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

class DeadAnimalException(Exception):
    pass

# HELPERS
def get_xy_coordinates(xy):
    x = None
    try:
        if 1 <= int(xy[0]) < 8:
            x = xy[0]
        else:
            raise IndexError
        y = xy[1]
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        return (int(x), arr.index(y) + 1)
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
    in_row =  (1 <= int(col) < 8)
    in_col =  (1 <= int(row) < 10)
    res =  in_row and in_col
    # print "in row (1 <= (row:%s) < 8) = %s , (1 <= (col:%s) < 10) = %s  " % (row, in_row, col, in_col)
    return res


class Animal(object):
    """docstring for Animal"""
    def __init__(self, _type, owner=None, verbose=False):
        self._type = _type
        self._capturable = ['Den']
        self._verbose = verbose
        self.position = None
        self.location = None
        self.owner = owner
        self.is_dead = False
        # self.get_initial_location()

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
            print self.can_capture(other_animal)
            return True

    def get_initial_location(self):
        self.location = INITIAL_LOCATIONS[self.owner][self.get_symbol()]
        return self.location


    def can_move_to(self, new_location):
        ''' returns (status, (new_row, new_col)) '''
        try:
            if self.is_dead:
                raise DeadAnimalException("\nDear %s, \n Sorry I'm dead.\n \t ~love your dead %s" % (self.owner, self._type))

            cur_row, cur_col = get_xy_coordinates(self.location)[::-1]
            new_row, new_col = get_xy_coordinates(new_location)[::-1]
            #  left, up , right , down
            print cur_row, cur_col
            print new_row, new_col
            _neighbor = [
                (cur_row, cur_col-1),
                (cur_row-1, cur_col),
                (cur_row, cur_col+1),
                (cur_row+1, cur_col)
            ]
            neighbor = []
            [neighbor.append(item) for item in _neighbor if in_board(*item)]
            # print _neighbor, neighbor
            # print [get_alpha_numeric_coordinates(*x) for x in neighbor]
            return ((new_row, new_col) in neighbor, (new_row, new_col))
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

    def is_captured(self):
        self.is_dead = True

    def get_symbol(self):
        return self._type[0].upper()

    def get_position(self):
        return self.position

# class Empty(Animal):
#     def __init__(self, owner=None, verbose=False):
#         super(Wolf, self).__init__(self.__class__.__name__, owner=owner,
#                                    verbose=verbose)
#         self._capturable += []


class Den(Animal):
    """docstring for Den"""
    def __init__(self, owner=None, verbose=False):
        super(Den, self).__init__(self.__class__.__name__, owner=owner,
                                   verbose=verbose)
        self._capturable = []
    def __repr__(self):
        return '%s' % ('DEN' if self.owner.lower() == 'player1' else 'den')


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


class AnimalChecker(object):
    """docstring for AnimalChecker"""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._board = []
        self._y_arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self.player = []
        self.setup()
        self.plys = 0

    def setup(self):

        self._board = self.build_board()
        self.players = self.init_players()
        for _player in self.players:
            self._move_animal(_player.tiger, _player.tiger.get_initial_location())
            self._move_animal(_player.mouse, _player.mouse.get_initial_location())
            self._move_animal(_player.wolf, _player.wolf.get_initial_location())
            self._move_animal(_player.elephant, _player.elephant.get_initial_location())

            self._set_den(_player)

    def init_players(self):
        Player1 = Player('player1')
        Player2 = Player('player2')
        return [Player1, Player2]

    def _set_den(self, player):
        # get den location for this player
        player.den.location = INITIAL_LOCATIONS[player.name]['DEN']  # change location
        self._add_to_board(*get_xy_coordinates(player.den.location)[::-1],
                               content=player.den)  # remote  animal from previous location on board



    def get_players(self):
        return self.players

    def build_board(self):
        _board = []
        for row in xrange(0, self.rows):
            _board.append([])
            for col in xrange(0, self.cols):
                _board[row].append('   ')
        return _board

    def display_board(self):
        board_str = "\n[==============%s==============]\n\n" % (self.plys)
        for row_index in xrange(0, len(self._board)):
            row = self._board[row_index]

            curren_col = ''
            if(row_index == 0):  # just to display the first header line
                curren_col += '   |'
                for col_index in xrange(0, len(self._board[row_index])):
                    curren_col += ' ' + str(col_index + 1) + ' |'
                curren_col += '\n'

            curren_col += '' + self._y_arr[row_index] + "->|"
            for col in row:
                curren_col += '' + str(col) + '|'
             # curren_col
            board_str += '%s\n' % curren_col

        board_str += "\n[==============%s==============]\n" % self.plys
        print board_str

    # def display_board(self):
    #     for row_index in xrange(0, len(self._board)):
    #         row = self._board[row_index]

    #         curren_col = ''
    #         if(row_index == 0):  # just to display the first header line
    #             curren_col += '   |'
    #             for col_index in xrange(0, len(self._board[row_index])):
    #                 curren_col += ' ' + str(col_index + 1) + ' |'
    #             curren_col += '\n'

    #         curren_col += '' + self._y_arr[row_index] + "->|"
    #         for col in row:
    #             curren_col += '' + str(col) + '|'
    #         print curren_col

    def _add_to_board(self, row, col, content):
        try:
            # print "adding to board {%s,%s} = %s(%s)" % (row, col, content, content.owner)
            self._board[row - 1][col - 1] = content
        except IndexError:
            raise InvalidMoveException

    def get_item_at(self, row, col):
        return self._board[row - 1][col - 1]


    def _move_animal(self, animal, where):
        ''' each animal keep track of it's last position '''
        try:

            self._add_to_board(*get_xy_coordinates(animal.location)[::-1],
                               content='   ')  # remote  animal from previous location on board
            animal.location = where  # change location
            self._add_to_board(*get_xy_coordinates(where)[::-1],
                               content=animal)  # add animal to new location
        except Exception, e:
            raise e

    def move(self, who, new_location):
        try:
            # swapping x and y because x = col, y = row
            # status, (row, col) =
            # print new_location
            status, (row, col) = who.can_move_to(new_location)
            # print status
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
                    self._move_animal(who, new_location)

                    # who.location = new_location
                    # self._add_to_board(*get_xy_coordinates(new_location)[::-1],
                    #                    content=who)
                else:
                    print "can't do this - %s , %s" % (res, who.owner is not animal_on_tile.owner)
            else:  # tile was empty ... just move up there if you can
                self._move_animal(who, new_location)
            self.plys +=1
            self.display_board()
            return True
        except Exception, e:
            print traceback.format_exc(e)
            self.display_board()
            return False
            # raise e


try:
    # T = Tiger(verbose=True)
    # E = Elephant(verbose=True)
    # W = Wolf(verbose=True)
    # M = Mouse(verbose=True)

    # Player1 = Player('player1')
    # Player2 = Player('player2')

    # # print Player1.tiger
    # # print Player1.wolf
    # # print T.capturable
    # # print T.can_capture('elephant')
    # # print T.can_capture('WOLF')
    # # print T > E , T > W, T > M
    # # print E > T, E > M
    # # print T.get_symbol()
    # # print M.get_symbol()

    # # print '%s' % T
    game = AnimalChecker(rows=9, cols=7)
    # game.setup()
    p1, p2 = game.get_players()
    print game.display_board()
    game.move(p1.tiger, "6h")
    game.move(p2.wolf, "6b")
    game.move(p2.wolf, "6c")
    game.move(p2.wolf, "6d")
    game.move(p2.wolf, "6e")
    game.move(p2.wolf, "6f")
    game.move(p2.wolf, "6g")
    game.move(p1.tiger, "6g")
    print "content = ", game._board[6][5]
    game.move(p2.wolf, "7g")
    print "content = ", game._board[6][5]
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
    print "invalid move, try again"
