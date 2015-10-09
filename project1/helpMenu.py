import sys
import argparse

_description = " "

parser = argparse.ArgumentParser(prog="AnimalChercker", description=_description)
# parser.add_argument("-a", "--AI", nargs=1, help="set which player should the AI be [1,2]]")
parser.add_argument("-f", "--FirstPlayer", nargs=1, help="specify the player to play first [1 , 2]")


