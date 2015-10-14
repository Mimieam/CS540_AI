
class InvalidUserInputError(Exception):
    pass

class InvalidMoveException(Exception):
    pass


class OutOfBoardException(Exception):
    pass


class DeadAnimalException(Exception):
    pass


def get_board_string_state(game):
    return game.display_board(raw=True, no_print=True).replace('   ', '.')\
    .replace(' ', '').replace('den','d').replace('DEN','D')\
    .replace('|','').replace('*', '').strip()

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
        'up': (cur_row-1, cur_col) if in_board(cur_row-1, cur_col) else None,
        'down': (cur_row+1, cur_col) if in_board(cur_row+1, cur_col) else None,
        'left': (cur_row, cur_col-1) if in_board(cur_row, cur_col-1) else None,
        'right': (cur_row, cur_col+1) if in_board(cur_row, cur_col+1) else None
    }


def AI_getBestMove(current_game_state):
    return sef(current_game_state)


# this class sole purpose is to keep track of which move just happened
# component of the man  Animal checker class
class move_tracker(object):
    def __init__(self, game):
        self.game = game
        self.curr_move = {}
        self.move_log = []

    def __repr__(self):
        return " last move = %s" % self.curr_move

    def update(self, _who, _from, _where, _captured_animal=None):
        self.curr_move = {
            'who': _who,
            'from': _from,
            'where': _where,
            'captured': _captured_animal,
        }

        # append at the end
        self.move_log.append(self.curr_move)
        # print "(%s)[%s] moved from %s to %s, old content = {%s}" % (_who, _who.owner, _from, _where, _captured_animal)

    def free_captured(self):
        self.captured.is_dead = False

    def revert(self):
        ''' return the reverted move'''
        # print "rewinding last move..."
        # undo a move
        if not self.move_log:
            print "No move to rewind"
            return
        # pop a dictionary representing the last move
        last_move = self.move_log.pop()
        self.game._move_animal(last_move['who'], last_move['from'])
        # revive any Ghost
        if last_move['captured'] and not isinstance(last_move['captured'], str):
            last_move['captured'].is_dead = False
            self.game._move_animal(last_move['captured'], last_move['where'])

        self.curr_move = self.move_log[-1] if self.move_log else []
        self.game.plys -= 1
        return last_move

    def get_move_log(self):
        return self.move_log

    def get_board_from_player(self, _raw=True):
        staged_board = []
        for row in xrange(0, self.game.rows):
            staged_board.append([])
            for col in xrange(0, self.game.cols):
                staged_board[row].append('   ')

        for player in self.game.players:
            for _animal in player.__dict__ :
                if _animal not in ['name']:
                    r, c = player.__dict__[''+_animal]._row_col_location
                    # print r, c
                    # print [(player.__dict__[''+_animal]._row_col_location, player.__dict__[''+_animal])for _animal in player.__dict__ if _animal not in ['name']]
                    staged_board[r-1][c-1] = player.__dict__[''+_animal]
        # print staged_board

        # self.game.display_board(_board=staged_board, raw=_raw)


tigerAscii = '''
                                 ___..........__
           _,...._           _."'_,.++8n.n8898n.`"._        _....._
         .'       `".     _.'_.'" _.98n.68n. `"88n. `'.   ,"       `.
        /        .   `. ,'. "  -'" __.68`""'""=._`+8.  `.'     .     `.
       .       `   .   `.   ,d86+889" 8"""+898n, j8 9 ,"    .          \\
      :     '       .,   ,d"'"   _..d88b..__ `"868' .'  . '            :
      :     .      .    _    ,n8""88":8"888."8.  "               '     :
       \     , '  , . .88" ,8P'     ,d8. _   `"8n  `+.      `.   .     '
        `.  .. .     d89' "  _..n689+^'8n88n.._ `+  . `  .  , '      ,'
          `.  . , '  8'    .d88+"    j:""' `886n.    b`.  ' .' .   ."
           '       , .j            ,d'8.         `  ."8.`.   `.  ':
            .    .' n8    ,_      .f A 6.      ,..    `8b, '.   .'_
          .' _    ,88'   :8"8    6'.d`i.`b.   d8"8     688.  ".    `'
        ," .88  .d868  _         ,9:' `8.`8   "'  ` _  8+""      b   `,
      _.  d8P  d'  .d :88.     .8'`j   ;+. "     n888b 8  .     ,88.   .
     `   :68' ,8   88     `.   '   :   l `     .'   `" jb  .`   688b.   ',
    .'  .688  6P   98  =+""`.      `   '       ,-"`+"'+88b 'b.  8689  `   '
   ;  .'"888 .8;  ."+b. : `" ;               .: "' ; ,n  `8 q8, '88:       \\
   .   . 898  8:  :    `.`--"8.              d8`--' '   .d'  ;8  898        '
  ,      689  9:  8._       ,68 .        .  :89    ..n88+'   89  689,' `     .
  :     ,88'  88  `+88n  -   . .           .        " _.     6:  `868     '   '
  , '  .68h.  68      `"    . . .        .  . .             ,8'   8P'      .   .
  .      '88  'q.    _.f       .          .  .    '  .._,. .8"   .889        ,
 .'     `898   _8hnd8p'  ,  . ..           . .    ._   `89,8P    j"'  _   `
  \  `   .88, `q9868' ,9      ..           . .  .   8n .8 d8'   +'   n8. ,  '
  ,'    ,+"88n  `"8 .8'     . ..           . .       `8688P"   9'  ,d868'   .  .
  .      . `86b.    " .       .            ..          68'      _.698689;      :
   . '     ,889_.n8. ,  ` .   .___      ___.     .n"  `86n8b._  `8988'b      .,6
    '       q8689'`68.   . `  `:. `.__,' .:'  ,   +   +88 `"688n  `q8 q8.     88
    , .   '  "     `+8 n    .   `:.    .;'   . '    . ,89           "  `q,    `8
   .   .   ,        .    + c  ,   `:.,:"        , "   d8'               d8.    :
    . '  8n           ` , .         ::    . ' "  .  .68h.             .8'`8`.  6
     ,    8b.__. ,  .n8688b., .    .;:._     .___nn898868n.         n868b "`   8
      `.  `6889868n8898886888688898"' "+89n88898868868889'         688898b    .8
       :    q68   `""+8688898P ` " ' . ` '  ' `+688988P"          d8+8P'  `. .d8
       ,     88b.       `+88.     `   ` '     .889"'           ,.88'        .,88
        :    '988b        "88b.._  ,_      . n8p'           .d8"'      '     689
        '.     "888n._,      `"8"+88888n.8,88:`8 .     _ .n88P'   .  `      ;88'
         :8.     "q888.  .            "+888P"  "+888n,8n8'"      .  .     ,d986
         :.`8:     `88986                          `q8"           ,      :688"
         ;.  '8,      "88b .d                        '                  ,889'
         :..   `6n      '8988                                         b.89p
         :. .    '8.      `88b                                        988'
         :. .      8b       `q8.        '                     . '   .d89      '
         . .        `8:       `86n,.       " . ,        , "        ,98P      ,
         .. .         '6n.       +86b.        .      .         _,.n88'     .
           .            `"8b.      'q98n.        ,     .  _..n868688'          .
          ' . .            `"98.     `8868.       .  _.n688868898p"            d
           . .                '88.      "688.       q89888688868"            ,86
            '. .                 88.     `8898        " .889"'              .988
'''
